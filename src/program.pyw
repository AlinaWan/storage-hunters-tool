# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__author__ = "Riri"
__license__ = "MIT"

import atexit
import time
import tkinter as tk
import threading
from typing import final as sealed

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageTk

from core.constants import Constants
from core.config import Config
from core.native_methods import NativeMethods
from services.hotkey_listener import HotkeyListener
from ui.debug_window import DebugWindow
from ui.scan_area_overlay import ScanAreaOverlay
from ui.tooltip_marker import TooltipMarker
from utils.safe_message_box import SafeMessageBox

class Program:
    def __init__(self):
        self.should_exit = False
        self.is_active = False
        self.last_x = None
        self.last_time = None
        self.last_click_time = 0.0
        
        self.hotkey_listener = None
        self._hotkey_register_lock = threading.Lock()
        self._hotkey_registering = False
        
        self.last_hotkey_config = {
            "toggle": (Config.TOGGLE_MOD, Config.TOGGLE_KEY),
            "exit": (Config.EXIT_MOD, Config.EXIT_KEY),
            "debug": (Config.DEBUG_MOD, Config.DEBUG_KEY)
        }

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

    def _update_hotkey_registration(self):
        if self._hotkey_registering:
            return

        with self._hotkey_register_lock:
            self._hotkey_registering = True
            try:
                if self.hotkey_listener:
                    self.hotkey_listener.stop()
                    if self.hotkey_listener.is_alive():
                        self.hotkey_listener.join(timeout=1.0)

                self.hotkey_listener = HotkeyListener(
                    self.toggle_logic,
                    self.exit_logic,
                    lambda: None,  # menu
                    lambda: None,   # abort shutdown
                    self.debug_logic
                )
                self.hotkey_listener.start()
                self.hotkey_listener.status_event.wait(timeout=1.0)

                if not self.hotkey_listener.success:
                    self._handle_hotkey_retry()

            finally:
                self._hotkey_registering = False

    def run(self):
        marker = TooltipMarker()
        area_visual = ScanAreaOverlay(Config.SEARCH_REGION, 1.0)

        region_w = Config.SEARCH_REGION["width"]
        region_h = Config.SEARCH_REGION["height"]
        self.debug_window = DebugWindow(region_w, region_h, lambda: self.debug_window.toggle_visibility())

        self._update_hotkey_registration()

        print("[Program::Run] Initialized.")

        with mss() as sct:
            while not self.should_exit:
                self.debug_window.update()
                area_visual.update(self.is_active)
                now = time.perf_counter()

                sct_img = sct.grab(Config.SEARCH_REGION)
                frame = np.array(sct_img)
                
                bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
                hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
                
                mid_y_start = int(frame.shape[0] * 0.25)
                mid_y_end = int(frame.shape[0] * 0.75)
                
                slice_gray = gray[mid_y_start:mid_y_end, :]
                slice_sat = hsv[mid_y_start:mid_y_end, :, 1]
                slice_val = hsv[mid_y_start:mid_y_end, :, 2]

                line_mask = (slice_gray > 245)
                line_cols = np.where(np.any(line_mask, axis=0))[0]
                
                line_coords = None
                line_center_x = None
                line_confidence = 0.0
                
                if len(line_cols) > 0:
                    lx1 = int(np.min(line_cols))
                    lx2 = int(np.max(line_cols))
                    if (lx2 - lx1) < 20:
                        line_coords = (lx1, 2, lx2, frame.shape[0] - 2)
                        line_center_x = (lx1 + lx2) // 2
                        line_confidence = 1.0

                search_slice_height = slice_gray.shape[0]
                search_area_width = frame.shape[1]
                
                min_height_pixels = search_slice_height * (Config.MIN_TARGET_HEIGHT_PCT / 100.0)
                min_width_pixels = search_area_width * (Config.MIN_TARGET_WIDTH_PCT / 100.0)

                # High saturation + bright (handles Gold or Green targets)
                color_target_mask = (slice_sat > 75) & (slice_val > 140)
                # Low saturation + very bright (handles Silver targets)
                silver_target_mask = (slice_sat < 65) & (slice_val > 130)

                target_pixel_mask = color_target_mask | silver_target_mask

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
                
                col_sums = np.sum(target_pixel_mask, axis=0)
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
                        f"Target Bounding: {target_coords}\n"
                        f"Active State: {self.is_active}"
                    )
                    self.debug_window.update(target_pixel_mask, info_str)

                if line_center_x is not None:
                    global_cx = Config.SEARCH_REGION["left"] + line_center_x
                    velocity_pps = 0.0
                    
                    if self.last_x is not None and self.last_time is not None:
                        dt = now - self.last_time
                        if dt > 0:
                            velocity_pps = (global_cx - self.last_x) / dt
                    
                    self.last_x = global_cx
                    self.last_time = now
                    
                    # Intersect collision checks
                    if true_tx1 is not None and true_tx2 is not None:
                        if true_tx1 <= line_center_x <= true_tx2:
                            cooldown_seconds = Config.CLICK_COOLDOWN_MS / 1000.0
                            if (now - self.last_click_time) >= cooldown_seconds:
                                if self.is_active:
                                    NativeMethods.move_mouse(**Config.CLICK_COORDINATE, relative=False)
                                    NativeMethods.move_mouse(1, 1, relative=True)
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
                    
                time.sleep(0.005)

        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.debug_window.destroy()
        area_visual.root.destroy()
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