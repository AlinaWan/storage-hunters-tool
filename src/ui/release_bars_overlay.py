import tkinter as tk

from core.constants import Constants

class ReleaseBarsOverlay:
    def __init__(self, screen_w, screen_h):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")

        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        self.canvas = tk.Canvas(
            self.root,
            width=screen_w,
            height=screen_h,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()

        self.left_bar = None
        self.right_bar = None

    def draw_release_bars(self, x, y):
        if self.left_bar:
            self.canvas.delete(self.left_bar)
            self.canvas.delete(self.right_bar)

        size = int(Constants.SCREEN_WIDTH * (15 / 1920))
        gap = int(Constants.SCREEN_WIDTH * (12 / 1920))

        inner_boundary = gap
        outer_boundary = gap + size
        
        y_top = y - 1
        y_bottom = y + 1

        self.left_bar = self.canvas.create_rectangle(
            x - outer_boundary, y_top,
            x - inner_boundary, y_bottom,
            fill="yellow",
            outline=""
        )

        self.right_bar = self.canvas.create_rectangle(
            x + inner_boundary, y_top,
            x + outer_boundary, y_bottom,
            fill="yellow",
            outline=""
        )

    def update(self):
        self.root.update()
