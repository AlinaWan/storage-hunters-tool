import threading
from typing import final as sealed

from core.config import Config
from core.native_methods import NativeMethods

@sealed
class HotkeyListener(threading.Thread):
    def __init__(self, toggle_cb, exit_cb, menu_cb, cancel_shutdown_cb):
        super().__init__(daemon=True)
        self.toggle_cb = toggle_cb
        self.exit_cb = exit_cb
        self.menu_cb = menu_cb
        self.cancel_shutdown_cb = cancel_shutdown_cb
        
        self.status_event = threading.Event()
        self.success = False

    def stop(self):
        NativeMethods.post_thread_message(self.ident, NativeMethods.WM_QUIT, 0, 0)

    def run(self):
        # ID 1: F6 (Toggle Logic)
        # ID 2: Shift + Escape (Exit Logic)
        # ID 3: Ctrl + F10 (Menu Toggle)
        # ID 4: Escape (Cancel Shutdown)
        hotkeys = [
            (1, Config.TOGGLE_MOD, Config.TOGGLE_KEY, "Toggle"),
            (2, Config.EXIT_MOD, Config.EXIT_KEY, "Exit"),
            (3, Config.MENU_MOD, Config.MENU_KEY, "Menu"),
            (4, Config.CANCEL_SHUTDOWN_MOD, Config.CANCEL_SHUTDOWN_KEY, "Cancel Shutdown")
        ]

        registered_count = 0
        for hk_id, mod, key, name in hotkeys:
            if NativeMethods.register_hotkey(None, hk_id, mod, key):
                registered_count += 1
            else:
                print(f"[HotkeyListener] Failed to register {name} (ID: {hk_id}). Key might be in use.")

        # Even if only 1 registered, we should still run the loop
        if registered_count == 0:
            self.success = False
            self.status_event.set()
            return

        # Signal partial or full success
        self.success = (registered_count == len(hotkeys))
        self.status_event.set()

        msg = NativeMethods.create_msg()
        while NativeMethods.get_message(msg) != 0:
            if msg.message == NativeMethods.WM_HOTKEY:
                # Dispatch based on ID
                hk_id = msg.wParam
                if hk_id == 1: self.toggle_cb()
                elif hk_id == 2: self.exit_cb()
                elif hk_id == 3: self.menu_cb()
                elif hk_id == 4: self.cancel_shutdown_cb()
            
            NativeMethods.translate_message(msg)
            NativeMethods.dispatch_message(msg)
    
        # Cleanup only what we registered
        for hk_id, _, _, _ in hotkeys:
            NativeMethods.unregister_hotkey(None, hk_id)