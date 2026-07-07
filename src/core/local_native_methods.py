import ctypes
import os
from pathlib import Path
from typing import Final as ReadOnly, final as sealed

@sealed
class LocalNativeMethods:

    threshold_lib: ReadOnly = ctypes.CDLL(Path(__file__).resolve().parent.parent / "native" / "threshold.dll")

    threshold_lib.threshold.argtypes = [
        ctypes.c_void_p, # src
        ctypes.c_void_p, # dst
        ctypes.c_int,    # length
        ctypes.c_uint8   # threshold
    ]