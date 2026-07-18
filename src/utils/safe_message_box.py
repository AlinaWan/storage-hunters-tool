"""
Safe message box to prevent Python GIL crash.

Instead of calling NativeMethods.message_box():

- SafeMessageBox.show_message_box_async() (same arguments, plus callback)
- SafeMessageBox.show_message_box_sync() (same arguments)

Depends on message_box_worker.py in the same directory.
"""
import os
import sys
import subprocess
import threading
from enum import Enum, auto
from typing import final as sealed

class MessageBoxResult(Enum):
    SUCCESS = auto()
    WORKER_CRASHED = auto()
    EXECUTION_FAILED = auto()

@sealed
class SafeMessageBox():
    @staticmethod
    def show_message_box_async(text, title, flags, callback, topmost=False):
        def worker():
            try:
                worker_path = os.path.join(
                    "src\\native\\MessageBoxWorker.exe"
                )
                proc = subprocess.Popen(  
                    [  
                        worker_path,  
                        text,  
                        title,  
                        str(flags),
                        "1" if topmost else "0"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                stdout, stderr = proc.communicate()

                if proc.returncode != 0:
                    callback((MessageBoxResult.WORKER_CRASHED, None))
                    return

                result = int(stdout.strip())
                callback((MessageBoxResult.SUCCESS, result))

            except Exception:
                callback((MessageBoxResult.EXECUTION_FAILED, None))

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def show_message_box_sync(text, title, flags, topmost=False):
        try:
            worker_path = os.path.join(
                "src\\native\\MessageBoxWorker.exe"
            )

            proc = subprocess.Popen(  
                [  
                    worker_path,  
                    text,  
                    title,  
                    str(flags),
                    "1" if topmost else "0"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = proc.communicate()

            if proc.returncode != 0:
                return MessageBoxResult.WORKER_CRASHED, None

            return MessageBoxResult.SUCCESS, int(stdout.strip())

        except Exception:
            return MessageBoxResult.EXECUTION_FAILED, None