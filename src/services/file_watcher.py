import os
import time
import threading
from typing import final as sealed

from core.interfaces import IDisposable
from core.native_methods import NativeMethods
from utils.logger_mixin import LoggerMixin

@sealed
class FileWatcher(LoggerMixin, IDisposable):
    def __init__(self):
        self._thread = None
        self._cts = threading.Event()
        self._h_stop_event = None
        self._current_path = None

    def stop(self):
        # cancellation request
        self._cts.set()

        if self._h_stop_event:
            NativeMethods.set_event(self._h_stop_event)

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

        if self._thread and self._current_path is not None:
            self.logger.info(f"Watcher instance stopped for: {self._current_path}")

        self._thread = None

    def dispose(self):
        self.stop()

        # release owned state
        self._cts = threading.Event()
        self._current_path = None

    def start(self, file_path, on_change_callback):
        self.stop()

        # reuse watcher
        self._cts.clear()
        self._current_path = file_path

        self._thread = threading.Thread(
            target=self._watch_loop,
            args=(file_path, on_change_callback),
            daemon=True,
        )
        self._thread.start()

    def _watch_loop(self, path_to_watch, on_change_callback):
        path_to_watch = os.path.abspath(path_to_watch)
        
        is_dir = os.path.isdir(path_to_watch)
        dir_to_watch = path_to_watch if is_dir else os.path.dirname(path_to_watch)
        target_name = "" if is_dir else os.path.basename(path_to_watch).lower()

        self._h_stop_event = NativeMethods.create_event(manual_reset=True, initial_state=False)
        h_overlap_event = NativeMethods.create_event(manual_reset=True, initial_state=False)

        hDir = NativeMethods.open_directory_handle(dir_to_watch)
        if not hDir or hDir == NativeMethods.INVALID_HANDLE_VALUE:
            return

        overlapped = NativeMethods.create_overlapped(h_overlap_event)
        buffer = NativeMethods.create_buffer()

        try:
            while not self._cts.is_set():
                NativeMethods.read_directory_changes(hDir, buffer, NativeMethods.byref(overlapped))

                handles = [h_overlap_event, self._h_stop_event]
                result = NativeMethods.wait_for_multiple_objects(handles, wait_all=False)

                if result == 0: 
                    raw_name = NativeMethods.get_filename_from_notify_buffer(buffer)
                    self.logger.info(f"OS reported change in: {raw_name}")
                    full_path = os.path.join(dir_to_watch, raw_name)

                    if is_dir or raw_name.lower() == target_name:
                        time.sleep(0.1) 
                        on_change_callback(full_path)

                    NativeMethods.reset_event(h_overlap_event)
                else: 
                    NativeMethods.cancel_io(hDir)
                    break
        finally:
            NativeMethods.close_handle(hDir)
            NativeMethods.close_handle(h_overlap_event)
            NativeMethods.close_handle(self._h_stop_event)
            self._h_stop_event = None