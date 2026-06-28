import tkinter as tk
from tkinter import Label, Frame

import cv2
from PIL import Image, ImageTk

from core.config import Config

class DebugWindow:
    def __init__(self, width: int, height: int, on_close_callback):
        self.root = tk.Toplevel()
        self.root.title("Debug Mask")
        self.root.attributes("-topmost", True)
        self.root.withdraw() 
        
        self._is_actually_visible = False
        self.pending_toggle = False
        
        debug_width = width
        debug_height = height + 100
        self.root.geometry(f"{debug_width}x{debug_height}")
        self.root.configure(bg="black")
        
        self.debug_label = Label(self.root, bg="black")
        self.debug_label.pack(fill=tk.BOTH, expand=False)

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
        self.root.protocol("WM_DELETE_WINDOW", on_close_callback)

    def toggle_visibility(self):
        self.pending_toggle = True

    def update(self, mask_np=None, info_text=""):
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
            self.detection_info_label.configure(text=info_text)

        except Exception:
            pass

    def destroy(self):
        if self.root.winfo_exists():
            self.root.destroy()