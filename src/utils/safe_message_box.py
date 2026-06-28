"""
Safe message box to prevent Python GIL crash.

Instead of calling NativeMethods.message_box():

- SafeMessageBox.show_message_box_async() (same arguments plus callback)
- SafeMessageBox.show_message_box_sync() (same arguments)

Depends on message_box_worker.py in the same directory.
"""
import os
import sys
import subprocess
import threading

class SafeMessageBox:
    @staticmethod
    def show_message_box_async(text, title, flags, callback):
        def worker():
            try:
                worker_path = os.path.join(
                    os.path.dirname(__file__),
                    "message_box_worker.py"
                )

                proc = subprocess.Popen(
                    [
                        sys.executable,
                        worker_path,
                        text,
                        title,
                        str(flags)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                stdout, stderr = proc.communicate()

                if proc.returncode != 0:
                    print("[SafeMessageBox] Worker crashed:", stderr)
                    callback(None)
                    return

                result = int(stdout.strip())
                callback(result)

            except Exception as e:
                print(f"[SafeMessageBox] Failed: {e}")
                callback(None)

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def show_message_box_sync(text, title, flags):
        try:
            worker_path = os.path.join(
                os.path.dirname(__file__),
                "message_box_worker.py"
            )

            proc = subprocess.Popen(
                [
                    sys.executable,
                    worker_path,
                    text,
                    title,
                    str(flags)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate()

            if proc.returncode != 0:
                print("[SafeMessageBox] Worker crashed:", stderr)
                return None

            return int(stdout.strip())

        except Exception as e:
            print(f"[SafeMessageBox] Failed: {e}")
            return None