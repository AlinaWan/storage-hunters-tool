import tkinter as tk
from typing import final as sealed

from core.config import Config

@sealed
class TooltipMarker:
    _MARKER_HEIGHT_PX = 10
    _X_OFFSET = 20
    _Y_OFFSET = Config.TOOLTIP_MARKER_Y_OFFSET_PX

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-transparentcolor", "black")

        self.top_padding = self._Y_OFFSET + 20
        self.w = Config.SEARCH_REGION["width"] + 40
        self.h = Config.SEARCH_REGION["height"] + self.top_padding + 50
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.target_lines = []
        self.slider_line = None
        self.debug_text = self.canvas.create_text(10, self.h - 60, anchor="nw", fill="lime", font=("Consolas", 9))

    def update_overlay(self, line_coords, target_coords, velocity=0.0, confidence=0.0):
        if self.target_lines:
            for line in self.target_lines:
                self.canvas.delete(line)
            self.target_lines.clear()

        if self.slider_line:
            self.canvas.delete(self.slider_line)
            self.slider_line = None

        if target_coords:
            tx1, ty1, tx2, ty2 = target_coords

            y1 = ty1 + self.top_padding - self._Y_OFFSET
            y2 = y1 + self._MARKER_HEIGHT_PX

            # left marker
            self.target_lines.append(
                self.canvas.create_line(tx1 + self._X_OFFSET, y1, tx1 + self._X_OFFSET, y2, fill="magenta", width=2)
            )

            # right marker
            self.target_lines.append(
                self.canvas.create_line(tx2 + self._X_OFFSET, y1, tx2 + self._X_OFFSET, y2, fill="magenta", width=2)
            )

        if line_coords:
            lx1, ly1, lx2, ly2 = line_coords

            mid_x = (lx1 + lx2) // 2

            y1 = ly1 + self.top_padding - self._Y_OFFSET
            y2 = y1 + self._MARKER_HEIGHT_PX

            self.slider_line = self.canvas.create_line(
                mid_x + self._X_OFFSET, y1,
                mid_x + self._X_OFFSET, y2,
                fill="lime",
                width=2
            )

        logic_str = (
            f"VELOCITY: {velocity:.1f} px/s\n"
            f"CONF:     {confidence * 100:.1f}%\n"
            f"TARGET:   {'FOUND' if target_coords else 'LOST'}"
        )
        self.canvas.itemconfig(self.debug_text, text=logic_str)

        pos_x = Config.SEARCH_REGION["left"] - self._X_OFFSET
        pos_y = Config.SEARCH_REGION["top"] - self.top_padding
        
        self.root.geometry(f"{self.w}x{self.h}+{pos_x}+{pos_y}")
        self.root.deiconify()
        self.root.update()

    def hide(self):
        self.root.withdraw()
        try:
            self.root.update()
        except Exception:
            pass