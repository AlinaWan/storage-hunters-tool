import tkinter as tk
from tkinter import Label, Frame
from typing import final as sealed

import cv2
import numpy as np
from PIL import Image, ImageTk

from core.config import Config

@sealed
class DebugWindow:
    def __init__(self, width: int, height: int, on_close_callback):
        self.root = tk.Toplevel()
        self.root.title("Debug Mask")
        self.root.attributes("-topmost", True)
        self.root.withdraw() 
        
        self._is_actually_visible = False
        self.pending_toggle = False
        
        debug_width = width
        debug_height = (height * 2) + 105
        self.root.geometry(f"{debug_width}x{debug_height}")
        self.root.configure(bg="black")
        
        # First image label (Original Binary Mask)
        self.debug_label = Label(self.root, bg="black")
        self.debug_label.pack(fill=tk.BOTH, expand=False)

        # Second image label (Target Box Highlighted Mask)
        self.debug_label2 = Label(self.root, bg="black")
        self.debug_label2.pack(fill=tk.BOTH, expand=False, pady=(5, 0))

        detection_frame = Frame(self.root, bg="black", pady=5)
        Label(
            detection_frame,
            text="Detection Information:",
            font=("Segoe UI", 10, "bold"),
            bg="black",
            fg="white",
        ).pack(anchor="w", padx=5)
        
        self.detection_info_label = Label(
            detection_frame,
            text="Status: Active",
            font=("Segoe UI", 9),
            bg="black",
            fg="lightgray",
            justify="left",
        )
        self.detection_info_label.pack(anchor="w", padx=10)
        detection_frame.pack(fill="x")

        self._current_img = None 
        self._current_img2 = None 
        self.root.protocol("WM_DELETE_WINDOW", on_close_callback)

    def toggle_visibility(self):
        self.pending_toggle = True

    def update(self, mask_np=None, info_text="", target_coords=None):
        if not self.root.winfo_exists():
            return

        if self.pending_toggle:
            self.pending_toggle = False
            if self._is_actually_visible:
                self.root.withdraw()
                self._is_actually_visible = False
            else:
                self.root.deiconify()
                self._is_actually_visible = True

        self.root.update()

        if mask_np is None or not self._is_actually_visible:
            return

        try:
            # --- Image 1: Original Binary Mask ---
            mask_uint8 = (mask_np * 255).astype("uint8")
            mask_uint8 = cv2.resize(
                mask_uint8,
                (Config.SEARCH_REGION["width"], Config.SEARCH_REGION["height"]),
                interpolation=cv2.INTER_NEAREST
            )
            img_pil = Image.fromarray(mask_uint8)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            self._current_img = img_tk
            self.debug_label.configure(image=img_tk)

            # --- Image 2: Target Box Magenta + Gray Rest ---
            colored_mask = cv2.cvtColor(mask_np.astype("uint8") * 255, cv2.COLOR_GRAY2RGB)
            
            white_pixels = (colored_mask == [255, 255, 255]).all(axis=-1)
            colored_mask[white_pixels] = [60, 60, 60]

            # 3. If a target bounding box is actively found, color that specific zone Magenta
            if target_coords is not None:
                # target_coords format from main loop: (tx1, 4, tx2, frame_height - 4)
                tx1, _, tx2, _ = target_coords
                
                # Highlight only the slice width columns where the target lives
                # We target the white pixels inside that column span to make them magenta
                box_zone_white = white_pixels[:, tx1:tx2]
                colored_mask[:, tx1:tx2][box_zone_white] = [255, 0, 255]

            # Resize the final canvas
            colored_mask = cv2.resize(
                colored_mask,
                (Config.SEARCH_REGION["width"], Config.SEARCH_REGION["height"]),
                interpolation=cv2.INTER_NEAREST
            )
            
            img_pil2 = Image.fromarray(colored_mask)
            img_tk2 = ImageTk.PhotoImage(image=img_pil2)

            self._current_img2 = img_tk2
            self.debug_label2.configure(image=img_tk2)
            
            self.detection_info_label.configure(text=info_text)

        except Exception:
            pass

    def destroy(self):
        if self.root.winfo_exists():
            self.root.destroy()