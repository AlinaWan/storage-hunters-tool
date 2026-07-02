import threading
from typing import final as sealed, override

from src.core.config import Config
from src.core.interfaces import IDisposable
from src.core.native_methods import NativeMethods

@sealed
class HotkeyListener(threading.Thread, IDisposable):
    def __init__(
        self,
        toggle_cb,
        exit_cb,
        menu_cb,
        cancel_shutdown_cb,
        debug_cb
    ):
        super().__init__(daemon=True)

        self.toggle_cb = toggle_cb
        self.exit_cb = exit_cb
        self.menu_cb = menu_cb
        self.cancel_shutdown_cb = cancel_shutdown_cb
        self.debug_cb = debug_cb

        self.status_event = threading.Event()
        self.success = False

        self._registered_hotkeys = []

    def stop(self):
        if self.ident is not None:
            NativeMethods.post_thread_message(
                self.ident,
                NativeMethods.WM_QUIT,
                0,
                0
            )

    def dispose(self):
        self.stop()

        if self.is_alive():
            self.join(timeout=1.0)

    def _register_hotkeys(self):
        # ID 1: Toggle Logic
        # ID 2: Exit Logic
        # ID 3: Menu Toggle
        # ID 4: Cancel Shutdown
        # ID 5: Debug Logic
        hotkeys = [
            (1, Config.TOGGLE_MOD, Config.TOGGLE_KEY, "Toggle"),
            (2, Config.EXIT_MOD, Config.EXIT_KEY, "Exit"),
            (3, Config.MENU_MOD, Config.MENU_KEY, "Menu"),
            (4, Config.CANCEL_SHUTDOWN_MOD, Config.CANCEL_SHUTDOWN_KEY, "Cancel Shutdown"),
            (5, Config.DEBUG_MOD, Config.DEBUG_KEY, "Toggle Debug"),
        ]

        registered = 0

        for hk_id, mod, key, name in hotkeys:
            if NativeMethods.register_hotkey(None, hk_id, mod, key):
                self._registered_hotkeys.append(hk_id)
                registered += 1
            else:
                self.logger.error(
                    f"Failed to register "
                    f"{name} (ID: {hk_id})"
                )

        self.success = registered > 0
        self.status_event.set()

        return registered > 0

    def _unregister_hotkeys(self):
        for hk_id in self._registered_hotkeys:
            NativeMethods.unregister_hotkey(None, hk_id)

        self._registered_hotkeys.clear()

    def _handle_hotkey(self, hk_id):
        if hk_id == 1:
            self.toggle_cb()
        elif hk_id == 2:
            self.exit_cb()
        elif hk_id == 3:
            self.menu_cb()
        elif hk_id == 4:
            self.cancel_shutdown_cb()
        elif hk_id == 5:
            self.debug_cb()

    @override
    def run(self):
        if not self._register_hotkeys():
            return

        msg = NativeMethods.create_msg()

        try:
            while NativeMethods.get_message(msg) != 0:
                if msg.message == NativeMethods.WM_HOTKEY:
                    self._handle_hotkey(msg.wParam)

                NativeMethods.translate_message(msg)
                NativeMethods.dispatch_message(msg)

        finally:
            self._unregister_hotkeys()