import ctypes
import os
import subprocess
import time

class AttachVsJitDebugger:
    @staticmethod
    def run():
        if os.getenv("ATTACHVSJITDEBUGGER") == "1":
            subprocess.Popen(["vsjitdebugger.exe", "-p", str(os.getpid())])
            while not ctypes.windll.kernel32.IsDebuggerPresent():
                time.sleep(0.1)