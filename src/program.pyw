# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__author__ = "Riri"
__license__ = "MIT"

import atexit
import signal
import time
import threading
from typing import final as sealed

import cv2
import numpy as np
import bettercam

from core.config import Config
from core.config_handler import ConfigHandler
from core.constants import Constants
from core.native_methods import NativeMethods
from services.hotkey_listener import HotkeyListener
from services.recache_manager import RecacheManager
from ui.debug_window import DebugWindow
from ui.menu_overlay import MenuOverlay
from ui.scan_area_overlay import ScanAreaOverlay
from ui.tooltip_marker import TooltipMarker
from utils.safe_message_box import SafeMessageBox

@sealed
class Program:
    def __init__(self):
        self.menu = None
        self.should_exit = False
        self.is_active = False
        self.last_x = None
        self.last_time = None
        self.last_click_time = 0.0
        self.velocity = 0.0

        self.click_tracking = None
        self.avg_latency = 0.0
        self.latest_debug_click_data = None

        self.hotkey_listener = None
        self._hotkey_register_lock = threading.Lock()
        self._hotkey_registering = False

        self._cache_lock = threading.Lock()
        self.recache_manager = RecacheManager()
        ConfigHandler.set_recache_manager(self.recache_manager)

        # values that need recache
        self.last_hotkey_config = {
            "toggle": (Config.TOGGLE_MOD, Config.TOGGLE_KEY),
            "exit": (Config.EXIT_MOD, Config.EXIT_KEY),
            "menu": (Config.MENU_MOD, Config.MENU_KEY),
            "debug": (Config.DEBUG_MOD, Config.DEBUG_KEY)
        }

        self.recache_manager.register(self._recache)

    def toggle_logic(self):
        self.is_active = not self.is_active
        print(f"[Program::Toggle] Toggled. Active: {self.is_active}")

    def exit_logic(self):
        print("[Program::Exit] Exit signaled.")
        self.should_exit = True

    def debug_logic(self):
        if hasattr(self, 'debug_window') and self.debug_window:
            self.debug_window.toggle_visibility()

    def _handle_hotkey_retry(self):
        def on_result(result):
            if result == 4:  # Retry clicked
                print("[Program::Hotkey] Retrying hotkey registration...")
                self._update_hotkey_registration()
            else:
                print("[Program::Hotkey] User bypassed hotkey warning configuration.")

        SafeMessageBox.show_message_box_async(
            "Failed to register one or more hotkeys.\n\n"
            "This is usually because another program is already using them. "
            "Please close conflicting apps or change your hotkeys and click 'Retry', or 'Cancel' to continue.",
            "Hotkey Warning",
            NativeMethods.MB_RETRYCANCEL | NativeMethods.MB_ICONWARNING,
            on_result
        )

    def _recache(self):
        with self._cache_lock:
            if hasattr(self, "area_visual"):
                self.area_visual.update_dimensions(Config.SEARCH_REGION, 1.0)

            self._update_hotkey_registration()

            print("[Program::Recache] Cache rebuilt")

    def _update_hotkey_registration(self):
        if self._hotkey_registering:
            print("[Program::Hotkey] Registration already in progress, skipping...")
            return

        with self._hotkey_register_lock:
            self._hotkey_registering = True

            try:
                current_config = {
                    "toggle": (Config.TOGGLE_MOD, Config.TOGGLE_KEY),
                    "exit": (Config.EXIT_MOD, Config.EXIT_KEY),
                    "menu": (Config.MENU_MOD, Config.MENU_KEY),
                    "debug": (Config.DEBUG_MOD, Config.DEBUG_KEY)
                }

                if current_config == self.last_hotkey_config and self.hotkey_listener is not None:
                    return

                print("[Program::Hotkey] Re-registering hotkeys...")

                # stop old listener safely
                if self.hotkey_listener:
                    self.hotkey_listener.stop()
                    if self.hotkey_listener.is_alive():
                        self.hotkey_listener.join(timeout=1.0)

                # attempt registration
                self.hotkey_listener = HotkeyListener(
                    self.toggle_logic,
                    self.exit_logic,
                    self.menu.toggle,
                    lambda: None, # abort shutdown
                    self.debug_logic
                )
                self.hotkey_listener.start()

                # wait briefly for result
                self.hotkey_listener.status_event.wait(timeout=1.0)

                if self.hotkey_listener.success:
                    self.last_hotkey_config = current_config
                    return

                # failure → async retry (NON-BLOCKING)
                self._handle_hotkey_retry()

            finally:
                self._hotkey_registering = False

    def run(self):
        marker = TooltipMarker()
        self.menu = MenuOverlay(ConfigHandler.load_config, ConfigHandler.edit_config, ConfigHandler.open_help)

        region_w = Config.SEARCH_REGION["width"]
        region_h = Config.SEARCH_REGION["height"]
        self.debug_window = DebugWindow(region_w, region_h, lambda: self.debug_window.toggle_visibility())
        self.area_visual = ScanAreaOverlay(Config.SEARCH_REGION, 1.0)

        self._recache()

        print("[Program::Run] Initialized.")

        # initialize bettercam with BGRA output format to match OpenCV pipeline
        camera = bettercam.create(output_color="BGRA")

        # convert the mss-style dict (left, top, width, height) to bettercam tuple format (left, top, right, bottom)
        region = (
            Config.SEARCH_REGION["left"],
            Config.SEARCH_REGION["top"],
            Config.SEARCH_REGION["left"] + Config.SEARCH_REGION["width"],
            Config.SEARCH_REGION["top"] + Config.SEARCH_REGION["height"]
        )

        while not self.should_exit:
            self.recache_manager.flush()
            self.debug_window.update()
            self.area_visual.update(self.is_active)
            if self.menu.alive:
                self.menu.update()

            now = time.perf_counter()

            # Grab frame using bettercam
            frame = camera.grab(region=region)
            if frame is None:
                continue
            
            bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
                
            mid_y_start = int(frame.shape[0] * 0.25)
            mid_y_end = int(frame.shape[0] * 0.75)
                
            slice_gray = gray[mid_y_start:mid_y_end, :]
            slice_val = hsv[mid_y_start:mid_y_end, :, 2]

            line_mask = (slice_gray > 245)
            line_cols = np.where(np.any(line_mask, axis=0))[0]
                
            line_coords = None
            line_center_x = None
            line_confidence = 0.0
                
            if len(line_cols) > 0:
                lx1 = int(np.min(line_cols))
                lx2 = int(np.max(line_cols))
                if (lx2 - lx1) < Config.MAX_LINE_WIDTH_PX:
                    line_coords = (lx1, 2, lx2, frame.shape[0] - 2)
                    line_center_x = (lx1 + lx2) // 2
                    line_confidence = 1.0

            search_slice_height = slice_gray.shape[0]
            search_area_width = frame.shape[1]
                
            min_height_pixels = search_slice_height * (Config.MIN_TARGET_HEIGHT_PCT / 100.0)
            min_width_pixels = search_area_width * (Config.MIN_TARGET_WIDTH_PCT / 100.0)

            # main masking
            slice_val_8u = slice_val.astype(np.uint8)
            # otsu binarization
            _, target_pixel_mask = cv2.threshold(
                slice_val_8u, 
                0, 
                255, 
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            # simple clean up using opening operation
            kernel = np.ones((3, 3), np.uint8)
            target_pixel_mask = cv2.morphologyEx(
                target_pixel_mask,
                cv2.MORPH_OPEN,
                kernel
            ).astype(bool)

            col_sums_raw = np.sum(target_pixel_mask, axis=0)
            active_columns_raw = np.where(col_sums_raw > min_height_pixels)[0]
                
            true_tx1, true_tx2 = None, None
            if len(active_columns_raw) > 0:
                clusters_raw = np.split(active_columns_raw, np.where(np.diff(active_columns_raw) > 5)[0] + 1)
                if clusters_raw and len(clusters_raw[0]) > 0:
                    largest_cluster_raw = max(clusters_raw, key=len)
                    if len(largest_cluster_raw) >= min_width_pixels:
                        true_tx1 = int(largest_cluster_raw[0])
                        true_tx2 = int(largest_cluster_raw[-1])

            if line_center_x is not None:
                ignore_left = max(0, line_center_x - Config.LINE_BLIND_BUFFER_PX)
                ignore_right = min(frame.shape[1], line_center_x + Config.LINE_BLIND_BUFFER_PX)
                target_pixel_mask[:, ignore_left:ignore_right] = False
                
            col_sums = np.count_nonzero(target_pixel_mask, axis=0)
            active_columns = np.where(col_sums > min_height_pixels)[0]
                
            target_coords = None
            if len(active_columns) > 0:
                clusters = np.split(active_columns, np.where(np.diff(active_columns) > 5)[0] + 1)
                if clusters and len(clusters[0]) > 0:
                    largest_cluster = max(clusters, key=len)
                    if len(largest_cluster) >= min_width_pixels:
                        target_coords = (int(largest_cluster[0]), 4, int(largest_cluster[-1]), frame.shape[0] - 4)

            if target_coords is None and true_tx1 is not None:
                target_coords = (true_tx1, 4, true_tx2, frame.shape[0] - 4)

            if self.debug_window:
                info_str = (
                    f"Line Center X: {line_center_x}\n"
                    f"Line Velocity: {self.velocity}\n"
                    f"Target Bounding: {target_coords}\n"
                    f"Average Latency: {self.avg_latency * 1000.0:.1f}ms\n"
                    f"Active State: {self.is_active}"
                )
                self.debug_window.update(
                    target_pixel_mask, 
                    info_str, 
                    target_coords=target_coords, 
                    click_data=self.latest_debug_click_data,
                    current_frame=bgr[mid_y_start:mid_y_end, :]
                )

            if line_center_x is not None:
                global_cx = Config.SEARCH_REGION["left"] + line_center_x
                velocity_pps = 0.0
                    
                if self.last_x is not None and self.last_time is not None:
                    dt = now - self.last_time
                    if dt > 0:
                        raw_velocity = (global_cx - self.last_x) / dt
                        alpha = 0.05
                        self.velocity += alpha * (raw_velocity - self.velocity)
                        velocity_pps = self.velocity
                    
                self.last_x = global_cx
                self.last_time = now
                
                # latency calibration
                # Stability tracking routine after click execution
                if self.click_tracking is not None:
                    track = self.click_tracking

                    # Check if the line has settled visually (barely moved)
                    if abs(line_center_x - track["last_seen_x"]) <= 1:
                        track["stable_frames"] += 1
                    else:
                        track["stable_frames"] = 0

                    track["last_seen_x"] = line_center_x
                    track["final_x"] = line_center_x

                    # When the line has remained stationary for long enough (e.g., 3 frames)
                    if track["stable_frames"] >= 3:
                        self.latest_debug_click_data = (
                            track["fired_x"],
                            track["final_x"],
                            track["target"][0],
                            track["target"][1]
                        )

                        pixel_overshoot = abs(track["final_x"] - track["fired_x"])

                        if abs(track["fired_vel"]) > 1.0 and pixel_overshoot >= 2.0:
                            actual_lag_seconds = pixel_overshoot / abs(track["fired_vel"])
                            tx1, tx2 = track["target"]

                            if tx1 is not None and tx2 is not None:
                                # clicked too early
                                if (track["fired_vel"] > 0 and track["final_x"] < tx1) or (track["fired_vel"] < 0 and track["final_x"] > tx2):
                                    self.avg_latency = max(0.005, self.avg_latency * 0.85)
                                    print(f"[Program::Calibration] Clicked early. Adjusted: {self.avg_latency * 1000.0:.1f}ms")
                                
                                # clicked too late
                                elif (track["fired_vel"] > 0 and track["final_x"] > tx2) or (track["fired_vel"] < 0 and track["final_x"] < tx1):
                                    self.avg_latency = min(0.120, self.avg_latency * 1.15)
                                    print(f"[Program::Calibration] Clicked late. Adjusted: {self.avg_latency * 1000.0:.1f}ms")
                                
                                # hit case
                                else:
                                    if 0.002 <= actual_lag_seconds <= 0.120:
                                        alpha_smooth = 0.25
                                        self.avg_latency = (alpha_smooth * actual_lag_seconds) + ((1.0 - alpha_smooth) * self.avg_latency)
                                        print(f"[Program::Calibration] Engine Lag: {self.avg_latency * 1000.0:.1f}ms")

                        # Terminate tracking tracking until next click
                        self.click_tracking = None
                    
                # Intersect collision checks
                if true_tx1 is not None and true_tx2 is not None:

                    collision_x = line_center_x

                    if Config.USE_PREDICTIVE_COLLISION:
                        # project line forward using calibrated timing lag
                        # velocity = px/s, avg_latency = s → px offset
                        lead_pixels = self.velocity * self.avg_latency
                        collision_x = max(
                            0,
                            min(frame.shape[1], int(line_center_x + lead_pixels))
                        )

                    if true_tx1 <= collision_x <= true_tx2:
                        cooldown_seconds = Config.CLICK_COOLDOWN_MS / 1000.0

                        if (now - self.last_click_time) >= cooldown_seconds:
                            if self.is_active:
                                NativeMethods.move_mouse(
                                    **Config.CLICK_COORDINATE,
                                    relative=False
                                )
                                NativeMethods.move_mouse(1, 1, relative=True)

                                self.click_tracking = {
                                    "fired_x": line_center_x,
                                    "fired_vel": self.velocity,
                                    "target": (true_tx1, true_tx2),
                                    "stable_frames": 0,
                                    "final_x": line_center_x,
                                    "last_seen_x": line_center_x
                                }

                                self.latest_debug_click_data = (line_center_x, None, true_tx1, true_tx2)

                                NativeMethods.send_mouse_click("left", True)
                                NativeMethods.send_mouse_click("left", False)

                                self.last_click_time = now
                    
                marker.update_overlay(
                    line_coords=line_coords,
                    target_coords=target_coords,
                    velocity=velocity_pps,
                    confidence=line_confidence
                )
            else:
                self.last_x = None
                self.last_time = None
                if target_coords:
                    marker.update_overlay(line_coords=None, target_coords=target_coords, velocity=0.0, confidence=0.0)
                else:
                    marker.hide()

        del camera
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.debug_window.destroy()
        self.area_visual.root.destroy()
        marker.root.destroy()

    def dispose(self):
        if self.hotkey_listener and self.hotkey_listener.is_alive():
            self.hotkey_listener.stop()

        from core.config_handler import config_watcher
        if config_watcher:
            config_watcher.stop()

        if self.mutex_handle:
            NativeMethods.release_mutex(self.mutex_handle)
            NativeMethods.close_handle(self.mutex_handle)

    @staticmethod
    def main():
        # This should be called BEFORE ANYTHING ELSE
        try:
            NativeMethods.set_process_dpi_awareness_context(-4)
        except Exception:
            pass

        mutex, is_first_instance = NativeMethods.create_single_instance_mutex(f"Global\\{Constants.GUID}")
        if not is_first_instance:
            SafeMessageBox.show_message_box_sync(
                "Another instance of Storage Hunters Tool is already running.",
                "Already Running",
                NativeMethods.MB_OK | NativeMethods.MB_ICONINFORMATION
            )
            raise SystemExit(0)

        app = Program()
        app.mutex_handle = mutex
        atexit.register(app.dispose)
        signal.signal(signal.SIGINT, lambda *_,: setattr(app, 'should_exit', True)) # exit cleanly

        try:
            app.run()
        except cv2.error as e:
            SafeMessageBox.show_message_box_sync(
                "An OpenCV error occurred during runtime:\n\n" +
                f"{e}\n\n" +
                "The program will now exit.",
                "Fatal Error",
                NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
            )
            raise

        except Exception as e:
            SafeMessageBox.show_message_box_sync(
                "An unexpected error occurred during runtime:\n\n" +
                f"{e}\n\n" +
                "The program will now exit.",
                "Fatal Error",
                NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
            )
            raise

if __name__ == "__main__":
    Program.main()