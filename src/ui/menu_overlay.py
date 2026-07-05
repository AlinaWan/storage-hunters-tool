import tkinter as tk
from typing import final as sealed

from src.core.native_methods import NativeMethods
from src.utils.date_time_util import DateTimeUtil

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
        self.after_ids = []

        # Bind Escape key to close the overlay instantly
        self.root.bind("<Escape>", lambda e: self.toggle())

        BG_COLOR = "#f8f9fa"
        TEXT_DARK = "#212529"
        LABEL_GREY = "#6c757d"
        BORDER_COLOR = "#dee2e6"
        PRESSED_COLOR = "#e9ecef"
        HOVER_COLOR = "#f1f3f5"  # subtle hover state color

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
            NativeMethods.register_drag_drop(hwnd, load_callback) # register this hwnd for drag drop
        except Exception:
            pass

        # Create a container frame for the headers to anchor them to the same exact grid space
        header_container = tk.Frame(self.root, bg=BG_COLOR)
        header_container.pack(pady=10)
        header_container.grid_columnconfigure(0, weight=1)
        header_container.grid_rowconfigure(0, weight=1)

        self.greeting = tk.Label(
            header_container,
            text="",
            font=("Segoe UI Variable Display", 15, "bold"),
            fg=BG_COLOR,
            bg=BG_COLOR
        )
        self.greeting.grid(row=0, column=0, sticky="nsew")

        self.header = tk.Label(
            header_container,
            text="What would you like to do?",
            font=("Segoe UI Variable Display", 15, "bold"),
            fg=BG_COLOR,
            bg=BG_COLOR
        )
        self.header.grid(row=0, column=0, sticky="nsew")

        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=5)

        def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
            points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
            return canvas.create_polygon(points, smooth=True, **kwargs)

        def create_button(parent, emoji, label_text, color, command, validator=None):
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

            # Visual feedback states
            def on_enter(e):
                canvas.itemconfig(rect, fill=HOVER_COLOR)

            def on_leave(e):
                canvas.itemconfig(rect, fill="white")

            def on_press(e):
                canvas.itemconfig(rect, fill=PRESSED_COLOR)
                canvas.move(icon, 1, 1)
                canvas.move(txt, 1, 1)

            def on_release(e):
                canvas.itemconfig(rect, fill=HOVER_COLOR) # Snap back to hover state color, not blank white
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

            canvas.bind("<Enter>", on_enter)
            canvas.bind("<Leave>", on_leave)
            canvas.bind("<Button-1>", on_press)
            canvas.bind("<ButtonRelease-1>", on_release)

            return container

        # Buttons
        create_button(btn_frame, "📥", "Import Config", "#4dabf7", load_callback)
        create_button(btn_frame, "✏️", "Edit Config", "#ff922b", edit_callback)
        create_button(btn_frame, "❓", "Get Help", "#f74d4d", save_callback)

        self.visible = False
        self.toggle_requested = False

    def _blend(self, start, end, t):
        s = tuple(int(start[i:i+2], 16) for i in (1,3,5))
        e = tuple(int(end[i:i+2], 16) for i in (1,3,5))

        rgb = tuple(
            int(s[i] + (e[i] - s[i]) * t)
            for i in range(3)
        )

        return "#%02x%02x%02x" % rgb

    def fade_label(self, label, fade_in=True, duration=350, callback=None):
        steps = 20
        delay = duration // steps

        def step(i):
            t = i / steps

            if not fade_in:
                t = 1 - t

            color = self._blend("#f8f9fa", "#212529", t)
            try:
                label.configure(fg=color)
            except tk.TclError:
                return

            if i < steps:
                after_id = self.root.after(delay, lambda: step(i + 1))
                self.after_ids.append(after_id)
            elif callback:
                callback()

        step(0)

    def play_header_animation(self):
        # Lift greeting to the top of the stack so it hides the header label underneath it
        self.greeting.tkraise()
        
        greeting_text = f"{DateTimeUtil.get_greeting()}, {NativeMethods.get_current_username()}"

        self.greeting.configure(
            text=greeting_text,
            fg="#f8f9fa"
        )

        self.header.configure(fg="#f8f9fa")

        self.fade_label(
            self.greeting,
            True,
            callback=lambda:
                # Save this transition pause ID so rapid open/closes clear cleanly
                self.after_ids.append(
                    self.root.after(
                        900,
                        lambda:
                            self.fade_label(
                                self.greeting,
                                False,
                                callback=lambda:
                                    # Raise the header back to the top right before fading it in
                                    (self.header.tkraise(), self.fade_label(self.header, True))
                            )
                    )
                )
        )

    def toggle(self):
        self.toggle_requested = True

    def _execute_toggle(self):
        if not self.alive:
            return

        try:
            if self.visible:
                for after_id in self.after_ids:
                    try:
                        self.root.after_cancel(after_id)
                    except Exception:
                        pass
                self.after_ids.clear()
                self.root.withdraw()
            else:
                self.root.deiconify()
                # Focus window on open so keyboard bindings like <Escape> work immediately
                self.root.focus_force() 
                self.play_header_animation()
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