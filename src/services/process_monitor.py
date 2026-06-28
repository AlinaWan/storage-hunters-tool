import threading
from typing import Callable, Optional

from core.native_methods import NativeMethods

class ProcessMonitor:
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._process_handle = None

    # ---------- Public API ----------

    @property
    def is_running(self) -> bool:
        """Returns True if the monitor thread is currently active."""
        return self._thread is not None and self._thread.is_alive()

    def start(self, pid: int, on_kill: Callable[[], None]):
        """Start monitoring a process by PID."""
        if self.is_running:
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._worker,
            args=(pid, on_kill),
            daemon=True
        )
        self._thread.start()

    def stop(self):
        """Stop monitoring."""
        self._stop_event.set()

        if self._process_handle:
            NativeMethods.close_handle(self._process_handle)
            self._process_handle = None

    # ---------- Internal ----------

    def _worker(self, pid: int, on_kill: Callable[[], None]):
        handle = NativeMethods.open_process(pid)

        if not handle:
            print("[ProcessMonitor] Failed to open process")
            return

        self._process_handle = handle

        print(f"[ProcessMonitor] Watching PID {pid}")

        NativeMethods.wait_for_single_object(handle)

        if self._stop_event.is_set():
            return

        print("[ProcessMonitor] Process exited")

        try:
            on_kill()
        finally:
            NativeMethods.close_handle(handle)
            self._process_handle = None
