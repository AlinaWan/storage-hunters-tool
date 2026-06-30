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
        debug_height = (height * 3) + 26 * 5 + 5 # about height/label, 26px/info line
        self.root.geometry(f"{debug_width}x{debug_height}")
        self.root.configure(bg="black")
        
        # First image label (Original Binary Mask)
        self.debug_label = Label(self.root, bg="black")
        self.debug_label.pack(fill=tk.BOTH, expand=False)

        # Second image label (Target Box Highlighted Mask)
        self.debug_label2 = Label(self.root, bg="black")
        self.debug_label2.pack(fill=tk.BOTH, expand=False, pady=(5, 0))

        # Third image label (Freeze Frame Capture with Click Indicators)
        self.debug_label3 = Label(self.root, bg="black")
        self.debug_label3.pack(fill=tk.BOTH, expand=False, pady=(5, 0))

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
        self._current_img3 = None 
        self.persistent_click_data = None # (click_fired_x, ended_up_x, tx1, tx2)
        self.freeze_frame = None          # Persistent raw frame storage

        self.root.protocol("WM_DELETE_WINDOW", on_close_callback)

    def toggle_visibility(self):
        self.pending_toggle = True

    def update(self, mask_np=None, info_text="", target_coords=None, click_data=None, current_frame=None):
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

            # --- Image 2: Target Box Assignment  ---
            colored_mask = cv2.cvtColor(mask_np.astype("uint8") * 255, cv2.COLOR_GRAY2BGR)
            
            white_pixels = (colored_mask == [255, 255, 255]).all(axis=-1)
            colored_mask[white_pixels] = [60, 60, 60]

            # If a target bounding box is actively found, color that specific zone Magenta (BGR: [255, 0, 255])
            if target_coords is not None:
                tx1, _, tx2, _ = target_coords
                box_zone_white = white_pixels[:, tx1:tx2]
                colored_mask[:, tx1:tx2][box_zone_white] = [255, 0, 255]

            # Update freeze state only on complete new click events
            if click_data is not None:
                # If this is a completely fresh click event (comparing fired_x and targets)
                if (self.persistent_click_data is None or 
                    self.persistent_click_data[0] != click_data[0] or 
                    self.persistent_click_data[2:] != click_data[2:]):
        
                    # Capture the background frame IMMEDIATELY on click fire
                    if current_frame is not None:
                        self.freeze_frame = current_frame.copy()
            
                # Always keep the click coordinates up-to-date (updates None -> final_x later)
                self.persistent_click_data = click_data

            # --- Image 3: Persistent Freeze Frame Window ---
            if self.freeze_frame is not None and self.persistent_click_data is not None:
                fired_x, ended_x, snap_tx1, snap_tx2 = self.persistent_click_data
                
                freeze_canvas = self.freeze_frame.copy()
                fh, fw, _ = freeze_canvas.shape
                
                # Pink lines for target area bounds
                if snap_tx1 is not None and 0 <= snap_tx1 < fw:
                    cv2.line(freeze_canvas, (snap_tx1, 0), (snap_tx1, fh), (203, 192, 255), 2)
                if snap_tx2 is not None and 0 <= snap_tx2 < fw:
                    cv2.line(freeze_canvas, (snap_tx2, 0), (snap_tx2, fh), (203, 192, 255), 2)
                # Red line for click fired
                if fired_x is not None and 0 <= fired_x < fw:
                    cv2.line(freeze_canvas, (fired_x, 0), (fired_x, fh), (0, 0, 255), 1)
                # Yellow line for "tracking line ended up" (will populate later if stable)
                if ended_x is not None and 0 <= ended_x < fw:
                    cv2.line(freeze_canvas, (ended_x, 0), (ended_x, fh), (0, 255, 255), 1)
                    
                freeze_canvas = cv2.resize(
                    freeze_canvas,
                    (Config.SEARCH_REGION["width"], Config.SEARCH_REGION["height"]),
                    interpolation=cv2.INTER_NEAREST
                )
                
                freeze_canvas_rgb = cv2.cvtColor(freeze_canvas, cv2.COLOR_BGR2RGB)
                img_pil3 = Image.fromarray(freeze_canvas_rgb)
                img_tk3 = ImageTk.PhotoImage(image=img_pil3)
                self._current_img3 = img_tk3
                self.debug_label3.configure(image=img_tk3)
            else:
                # initialize as black frame
                black_frame = np.zeros(
                    (Config.SEARCH_REGION["height"], Config.SEARCH_REGION["width"], 3), 
                    dtype=np.uint8
                )
                img_pil3 = Image.fromarray(black_frame)
                img_tk3 = ImageTk.PhotoImage(image=img_pil3)
                self._current_img3 = img_tk3
                self.debug_label3.configure(image=img_tk3)

            colored_mask = cv2.resize(
                colored_mask,
                (Config.SEARCH_REGION["width"], Config.SEARCH_REGION["height"]),
                interpolation=cv2.INTER_NEAREST
            )
            
            colored_mask_rgb = cv2.cvtColor(colored_mask, cv2.COLOR_BGR2RGB)
            img_pil2 = Image.fromarray(colored_mask_rgb)
            img_tk2 = ImageTk.PhotoImage(image=img_pil2)

            self._current_img2 = img_tk2
            self.debug_label2.configure(image=img_tk2)
            
            self.detection_info_label.configure(text=info_text)

        except Exception:
            pass

    def destroy(self):
        if self.root.winfo_exists():
            self.root.destroy()