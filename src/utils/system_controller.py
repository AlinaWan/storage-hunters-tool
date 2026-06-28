import threading

from core.native_methods import NativeMethods

class SystemController:
    def __init__(self):
        self._shutdown_cancel_event = threading.Event()

    def start_shutdown(self, timeout=15, message="Shutting down."):
        self._shutdown_cancel_event.clear()

        if not NativeMethods.enable_shutdown_privilege():
            print("[SystemController] Failed to enable privilege")
            return

        result = NativeMethods.initiate_system_shutdown(timeout, message)

        print(f"[SystemController] result: {result}")

        if not result:
            print("[SystemController] Shutdown call failed")
            return

        print("[SystemController] Shutdown scheduled")

        t = threading.Thread(
            target=self._wait_for_cancel,
            args=(timeout,),
            daemon=True
        )
        t.start()

    def cancel_shutdown(self):
        self._shutdown_cancel_event.set()

    def _wait_for_cancel(self, timeout):
        if self._shutdown_cancel_event.wait(timeout):
            NativeMethods.abort_system_shutdown()
            print("[SystemController] Shutdown cancelled")
