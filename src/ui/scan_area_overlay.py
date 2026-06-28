import tkinter as tk
from typing import final as sealed

from core.constants import Constants

@sealed
class ScanAreaOverlay:
    """Creates a persistent overlay showing the scan boundaries and 8 markers."""
    def __init__(self, area, scale):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-transparentcolor", "black")

        w = int(area['width'] / scale)
        h = int(area['height'] / scale)
        x = int(area['left'] / scale)
        y = int(area['top'] / scale)

        self.scale = scale
        self.offset_x = x
        self.offset_y = y

        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self.canvas = tk.Canvas(self.root, width=w, height=h, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.points = [
            (0, 0), (w//2, 0), (w, 0),
            (0, h//2), (w, h//2),
            (0, h), (w//2, h), (w, h)
        ]
        self.dots = []
        for px, py in self.points:
            size = int(Constants.SCREEN_HEIGHT * (4 / 1080)) # size of dots
            dot = self.canvas.create_rectangle(px-size, py-size, px+size, py+size, fill="red", outline="")
            self.dots.append(dot)

    def update(self, active):
        color = "green" if active else "red"
        for dot in self.dots:
            self.canvas.itemconfig(dot, fill=color)
        self.root.update()

    def update_dimensions(self, area, scale):
        w = int(area['width'] / scale)
        h = int(area['height'] / scale)
        x = int(area['left'] / scale)
        y = int(area['top'] / scale)

        # Resize the window
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.canvas.config(width=w, height=h)

        # Reposition the 8 red dots
        self.points = [
            (0, 0), (w//2, 0), (w, 0),
            (0, h//2), (w, h//2),
            (0, h), (w//2, h), (w, h)
        ]
        for i, (px, py) in enumerate(self.points):
            size = int(Constants.SCREEN_HEIGHT * (4 / 1080))
            self.canvas.coords(self.dots[i], px-size, py-size, px+size, py+size)
