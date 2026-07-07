import ctypes
import os
from pathlib import Path
from typing import Final as ReadOnly, final as sealed

@sealed
class LocalNativeMethods:
    """Local native methods for the specific Storage Hunters Tool application."""

    stvision: ReadOnly = ctypes.CDLL(Path(__file__).resolve().parent.parent / "native" / "stvision.dll")

    stvision.threshold.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_uint8] # src, dst, length, threshold
    stvision.threshold.restypes = None