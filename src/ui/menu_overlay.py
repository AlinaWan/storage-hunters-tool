import tkinter as tk
from typing import final as sealed

from core.config_handler import ConfigHandler
from core.native_methods import NativeMethods

@sealed
class MenuOverlay:
    def __init__(self, load_callback, edit_callback, save_callback):
        self.root = tk.Tk()
        self.root.withdraw() # Withdraw immediately to avoid flicker on startup; will show when toggled
        self.root.title("")
        self.root.protocol("WM_DELETE_WINDOW", self.toggle) # IMPORTANT: Use this to toggle or it will mess up the lifecycle and break the toggle functionality
        self.root.attributes("-toolwindow", True) # Keep a minimal title bar with only the close button and handle dragging the window
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.alive = True

        BG_COLOR = "#f8f9fa"
        TEXT_DARK = "#212529"
        LABEL_GREY = "#6c757d"
        BORDER_COLOR = "#dee2e6"
        PRESSED_COLOR = "#e9ecef"

        self.root.configure(bg=BG_COLOR)

        width, height = 380, 180
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        try:
            self.root.update_idletasks()
            hwnd = NativeMethods.get_parent(self.root.winfo_id()) # Get the actual window handle to apply
            NativeMethods.apply_rounded_corners(hwnd)
        except Exception:
            pass

        header = tk.Label(
            self.root,
            text="What would you like to do?",
            font=("Segoe UI Variable Display", 15, "bold"),
            fg=TEXT_DARK,
            bg=BG_COLOR,
            pady=10
        )
        header.pack()

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=5)

        def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
            points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
            return canvas.create_polygon(points, smooth=True, **kwargs)

        def create_button(parent, emoji, label_text, color, command, validator=None):
            self.after_ids = []

            size = 110
            radius = 20

            container = tk.Frame(parent, bg=BG_COLOR)
            container.pack(side="left", padx=5)

            canvas = tk.Canvas(
                container, width=size, height=size,
                bg=BG_COLOR, highlightthickness=0, cursor="hand2"
            )
            canvas.pack()

            rect = rounded_rect(canvas, 2, 2, size-2, size-2, radius, fill="white", outline=BORDER_COLOR)
            icon = canvas.create_text(size/2, size/2 - 10, text=emoji, font=("Segoe UI Emoji", 22), fill=color)
            txt = canvas.create_text(size/2, size/2 + 22, text=label_text, font=("Segoe UI Semibold", 8), fill=LABEL_GREY)

            original_label = label_text
            original_emoji = emoji # noqa: F841

            def on_press(e):
                canvas.itemconfig(rect, fill=PRESSED_COLOR)
                canvas.move(icon, 1, 1)
                canvas.move(txt, 1, 1)

            def on_release(e):
                canvas.itemconfig(rect, fill="white")
                canvas.move(icon, -1, -1)
                canvas.move(txt, -1, -1)

                if validator:
                    ok, msg = validator()
                    if not ok:
                        flash_message(msg)
                        return

                command()

            def flash_message(msg, duration=2000):
                canvas.itemconfig(txt, text=msg)

                def restore():
                    try:
                        canvas.itemconfig(txt, text=original_label)
                    except tk.TclError:
                        pass

                after_id = canvas.after(duration, restore)
                self.after_ids.append(after_id)

            canvas.bind("<Button-1>", on_press)
            canvas.bind("<ButtonRelease-1>", on_release)

            return container

        # Buttons
        create_button(btn_frame, "📥", "Import Config", "#4dabf7", ConfigHandler.load_config)
        create_button(btn_frame, "✏️", "Edit Config", "#ff922b", ConfigHandler.edit_config)
        create_button(btn_frame, "❓", "Get Help", "#f74d4d", ConfigHandler.open_help)

        self.visible = False
        self.toggle_requested = False

    def toggle(self):
        self.toggle_requested = True

    def _execute_toggle(self):
        if not self.alive:
            return

        try:
            if self.visible:
                self.root.withdraw()
            else:
                self.root.deiconify()
            self.visible = not self.visible
        except tk.TclError:
            self.alive = False

        self.toggle_requested = False

    def update(self):
        if not self.alive:
            return

        if self.toggle_requested:
            self._execute_toggle()

        try:
            self.root.update()
        except tk.TclError:
            self.alive = False
