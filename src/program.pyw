# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__author__ = "Riri"
__license__ = "MIT"

import time
import tkinter as tk
from typing import final as sealed

import cv2
from mss import mss
import numpy as np

from core.config import Config
from core.native_methods import NativeMethods
from ui.scan_area_overlay import ScanAreaOverlay
from ui.tooltip_marker import TooltipMarker
from utils.safe_message_box import SafeMessageBox

class Program:
    def __init__(self):
        self.should_exit = False
        self.is_active = True
        self.last_x = None
        self.last_time = None
        self.last_click_time = 0.0

    def run(self):
        marker = TooltipMarker()
        area_visual = ScanAreaOverlay(Config.SEARCH_REGION, 1.0)

        print("[Program::Run] Initialized.")

        with mss() as sct:
            while not self.should_exit:
                area_visual.update(self.is_active)
                now = time.perf_counter()
                
                if not self.is_active:
                    marker.hide()
                    time.sleep(0.1)
                    continue

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

                # -------------------------------------------------------------
                # PROCESS 1: DETECT THE WHITE SLIDER LINE
                # -------------------------------------------------------------
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

                # -------------------------------------------------------------
                # PROCESS 2: ISOLATE TARGET AREA W/ TRIPPABLE BOUNDS
                # -------------------------------------------------------------
                target_pixel_mask = (slice_sat > 40) | (slice_val > 130)
                
                # Extract true bounds for tracking/trigger BEFORE blinding
                col_sums_raw = np.sum(target_pixel_mask, axis=0)
                active_columns_raw = np.where(col_sums_raw > (slice_gray.shape[0] * 0.3))[0]
                
                true_tx1, true_tx2 = None, None
                if len(active_columns_raw) > 0:
                    clusters_raw = np.split(active_columns_raw, np.where(np.diff(active_columns_raw) > 5)[0] + 1)
                    if clusters_raw and len(clusters_raw[0]) > 0:
                        largest_cluster_raw = max(clusters_raw, key=len)
                        if len(largest_cluster_raw) > 15:
                            true_tx1 = int(largest_cluster_raw[0])
                            true_tx2 = int(largest_cluster_raw[-1])

                # Apply structural blind zone calculation to prevent trail bleeding
                if line_center_x is not None:
                    ignore_left = max(0, line_center_x - Config.BLIND_ZONE_RADIUS)
                    ignore_right = min(frame.shape[1], line_center_x + Config.BLIND_ZONE_RADIUS)
                    target_pixel_mask[:, ignore_left:ignore_right] = False
                
                col_sums = np.sum(target_pixel_mask, axis=0)
                active_columns = np.where(col_sums > (slice_gray.shape[0] * 0.3))[0]
                
                target_coords = None
                if len(active_columns) > 0:
                    clusters = np.split(active_columns, np.where(np.diff(active_columns) > 5)[0] + 1)
                    if clusters and len(clusters[0]) > 0:
                        largest_cluster = max(clusters, key=len)
                        if len(largest_cluster) > 15:
                            target_coords = (int(largest_cluster[0]), 4, int(largest_cluster[-1]), frame.shape[0] - 4)

                # Use unblinded fallback coordinates if blind zone covers the entire box visually
                if target_coords is None and true_tx1 is not None:
                    target_coords = (true_tx1, 4, true_tx2, frame.shape[0] - 4)

                if line_center_x is not None:
                    global_cx = Config.SEARCH_REGION["left"] + line_center_x
                    velocity_pps = 0.0
                    
                    if self.last_x is not None and self.last_time is not None:
                        dt = now - self.last_time
                        if dt > 0:
                            velocity_pps = (global_cx - self.last_x) / dt
                    
                    self.last_x = global_cx
                    self.last_time = now
                    
                    # Verify intersect against physical unblinded coordinates
                    if true_tx1 is not None and true_tx2 is not None:
                        if true_tx1 <= line_center_x <= true_tx2:
                            cooldown_seconds = Config.CLICK_COOLDOWN_MS / 1000.0
                            if (now - self.last_click_time) >= cooldown_seconds:
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

        area_visual.root.destroy()
        marker.root.destroy()

    @staticmethod
    def main():
        app = Program()
        try:
            app.run()
        except cv2.error as e:
            if "error: (-215:Assertion failed)" in str(e):
                SafeMessageBox.show_message_box_sync(
                    "OpenCV raised Error -215 (Assertion failed) during runtime.\n\n" +
                    "This is usually because DRAG_STEP resulted in a search area " +
                    "that is smaller than the template size. Try increasing DRAG_STEP, " + 
                    "decreasing DOWNSCALE_FACTOR, or using a smaller template image.\n\n" +
                    "The program will now close.",
                    "Fatal Error",
                    NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
                )
                raise 
            else:
                SafeMessageBox.show_message_box_sync(
                    "An OpenCV error occurred during runtime:\n\n" +
                    f"{e}\n\n" +
                    "The program will now close.",
                    "Fatal Error",
                    NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
                )
                raise

        except Exception as e:
            SafeMessageBox.show_message_box_sync(
                "An unexpected error occurred during runtime:\n\n" +
                f"{e}\n\n" +
                "The program will now close.",
                "Fatal Error",
                NativeMethods.MB_OK | NativeMethods.MB_ICONERROR
            )
            raise

if __name__ == "__main__":
    Program.main()