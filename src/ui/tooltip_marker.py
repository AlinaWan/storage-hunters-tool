import tkinter as tk
from typing import final as sealed

from core.config import Config

@sealed
class TooltipMarker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-transparentcolor", "black")

        self.w = Config.SEARCH_REGION["width"] + 40
        self.h = Config.SEARCH_REGION["height"] + 150
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.slider_line = None
        self.slider_box = None
        self.target_box = None
        self.debug_text = self.canvas.create_text(10, self.h - 60, anchor="nw", fill="lime", font=("Consolas", 9))

    def update_overlay(self, line_coords, target_coords, velocity=0.0, confidence=0.0):
        if self.slider_line: self.canvas.delete(self.slider_line)
        if self.slider_box: self.canvas.delete(self.slider_box)
        if self.target_box: self.canvas.delete(self.target_box)
        
        self.slider_line = None
        self.slider_box = None
        self.target_box = None

        if target_coords:
            tx1, ty1, tx2, ty2 = target_coords
            self.target_box = self.canvas.create_rectangle(
                tx1 + 20, ty1 + 20, tx2 + 20, ty2 + 20, 
                outline="magenta", width=2
            )

        if line_coords:
            lx1, ly1, lx2, ly2 = line_coords
            mid_x = (lx1 + lx2) // 2
            
            self.slider_box = self.canvas.create_rectangle(
                lx1 + 20, ly1 + 20, lx2 + 20, ly2 + 20, 
                outline="cyan", width=2
            )
            self.slider_line = self.canvas.create_line(
                mid_x + 20, ly1 + 20, mid_x + 20, ly2 + 20, 
                fill="lime", width=2
            )

        logic_str = (
            f"VELOCITY: {velocity:.1f} px/s\n"
            f"CONF:     {confidence * 100:.1f}%\n"
            f"TARGET:   {'FOUND' if target_coords else 'LOST'}"
        )
        self.canvas.itemconfig(self.debug_text, text=logic_str)

        pos_x = Config.SEARCH_REGION["left"] - 20
        pos_y = Config.SEARCH_REGION["top"] - 20
        
        self.root.geometry(f"{self.w}x{self.h}+{pos_x}+{pos_y}")
        self.root.deiconify()
        self.root.update()

    def hide(self):
        self.root.withdraw()
        try:
            self.root.update()
        except Exception:
            pass