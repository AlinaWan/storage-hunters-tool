import os
import re
import threading
import time
from typing import final as sealed, Callable, Dict

from services.file_watcher import FileWatcher

@sealed
class RobloxLogMonitor:
    def __init__(self):
        self._watcher = FileWatcher()
        self._log_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Roblox", "logs")
        self._current_log_path = None
        self._last_position = 0
        self._running = False
        self._poll_thread = None # we cannot reliably count on file_watcher because it only reports a change for these types of logs
                                 # if the log is (for example) open in notepad.exe and notepad.exe is also focused
                                 # unfortunately that's just due to how Roblox writes logs and we can't do anything about it
        
        # Maps compiled regex objects to their callback functions
        self._handlers: Dict[re.Pattern, Callable[[re.Match], None]] = {}

    @property
    def is_running(self) -> bool:
        """Exposes the internal running state to the RecacheManager."""
        return self._running

    def start(self, patterns_and_callbacks: Dict[str, Callable[[re.Match], None]]):
        if self._running:
            return

        # Compile patterns once on start
        self._handlers = {re.compile(p): c for p, c in patterns_and_callbacks.items()}
        self._running = True
        
        # Initialize by finding the current log and jumping to the end
        self._refresh_latest_log()
        
        # Start the directory watcher
        # The monitor will only wake up when the OS reports a file change
        self._watcher.start(self._log_dir, self._on_dir_change)

        # Start polling
        self._poll_thread = threading.Thread(target=self._internal_poll, daemon=True)
        self._poll_thread.start()

        print(f"[LogMonitor] Monitoring directory: {self._log_dir}")

    def stop(self):
        self._running = False
        self._watcher.stop()
        # The poll thread will exit on the next loop iteration
        print("[LogMonitor] Stopped.")

    def _internal_poll(self):
        """
        Periodically 'touches' the file to force a metadata sync.
        This triggers the OS FileWatcher to notice the change.
        (See remark at self._poll_thread initialization)
        """
        while self._running:
            if self._current_log_path and os.path.exists(self._current_log_path):
                try:
                    # Just opening and closing with share-ready permissions
                    # 'nudges' the OS just like Notepad does.
                    with open(self._current_log_path, "r", encoding="utf-8", errors="ignore") as _:
                        pass 
                except Exception:
                    pass
            time.sleep(1.0)

    def _on_dir_change(self, changed_path):
        if not self._running:
            return

        # Normalize paths for Windows comparison
        changed_path = os.path.normpath(changed_path)
        current_path = os.path.normpath(self._current_log_path) if self._current_log_path else None

        filename = os.path.basename(changed_path)
        if "_Player_" not in filename or not filename.endswith(".log"):
            return

        # If it's the file we are already tracking, just read the new lines
        if current_path and changed_path.lower() == current_path.lower():
            self._process_new_lines()
        else:
            # It's a new log file (Roblox likely restarted)
            self._current_log_path = changed_path
            # IMPORTANT: Start at 0 so we read the handshake/init lines!
            self._last_position = 0 
            print(f"[LogMonitor] Switching to new log: {filename}")
            self._process_new_lines()

    def _refresh_latest_log(self):
        if not os.path.exists(self._log_dir):
            return

        try:
            files = [
                os.path.join(self._log_dir, f) for f in os.listdir(self._log_dir) 
                if "_Player_" in f and f.endswith(".log")
            ]
            
            if not files:
                return

            latest_file = max(files, key=os.path.getmtime)

            # If Roblox switched to a new log file, reset position to the end of the new file
            if latest_file != self._current_log_path:
                self._current_log_path = latest_file
                self._last_position = os.path.getsize(latest_file)
                print(f"[LogMonitor] Tracking new log: {os.path.basename(latest_file)}")
        except Exception as e:
            print(f"[LogMonitor] Refresh Error: {e}")

    def _process_new_lines(self):
        if not self._current_log_path or not os.path.exists(self._current_log_path):
            return

        try:
            with open(self._current_log_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self._last_position)
                lines = f.readlines()
                self._last_position = f.tell()

                for line in lines:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    
                    # Debug: Show every line we found
                    # print(f"[LogMonitor::Read] {clean_line}")
                    self._parse_line(clean_line)
        except Exception as e:
            print(f"[LogMonitor] Read Error: {e}")

    def _parse_line(self, line: str):
        matched_any = False
        for pattern, callback in self._handlers.items():
            match = pattern.search(line)
            if match:
                # print(f"  └─ [Match] Pattern '{pattern.pattern}' triggered callback.")
                callback(match)
                matched_any = True
        
        if not matched_any:
            # print(f"  └─ [Skip] No handlers matched.")
            pass