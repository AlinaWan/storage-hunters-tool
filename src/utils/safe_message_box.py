"""
Safe message box to prevent Python GIL crash.

Instead of calling NativeMethods.message_box():

- SafeMessageBox.show_message_box_async() (SafeMessageBox, same arguments, plus callback)
- SafeMessageBox.show_message_box_sync() (SafeMessageBox, same arguments)

Depends on message_box_worker.py in the same directory.
"""
import logging
import os
import sys
import subprocess
import threading

from src.utils.logger_mixin import LoggerMixin

class SafeMessageBox(LoggerMixin):
    # this is a static class so we have to pass the logger through a small hack
    @property
    def logger(self):
        return logging.getLogger("SafeMessageBox")

    @classmethod
    def _get_logger(cls):
        if cls._factory is None:
            return logging.getLogger(f"{cls.__module__}.{cls.__qualname__}")
        name = f"{cls.__module__}.{cls.__qualname__}"
        return cls._factory.create_logger(name)

    @staticmethod
    def show_message_box_async(cls, text, title, flags, callback):
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
                    cls._get_logger().error(f"Worker crashed: {stderr}")
                    callback(None)
                    return

                result = int(stdout.strip())
                callback(result)

            except Exception as _:
                cls._get_logger().exception("Failed to execute worker")
                callback(None)

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def show_message_box_sync(cls, text, title, flags):
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
                cls._get_logger().error(f"Worker crashed: {stderr}")
                return None

            return int(stdout.strip())

        except Exception as _:
            cls._get_logger().exception("Failed to execute worker")
            return None