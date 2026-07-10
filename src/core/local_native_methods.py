import ctypes
import os
from pathlib import Path
from typing import Final as ReadOnly, final as sealed

@sealed
class LocalNativeMethods:
    """Local native methods for the specific Storage Hunters Tool application."""

    stvision: ReadOnly = ctypes.CDLL(Path(__file__).resolve().parent.parent / "native" / "stvision.dll")

    stvision.threshold.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_uint8] # src, dst, length, threshold
    stvision.threshold.restype = None

    stvision.find_line_bounds.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p] # src, width, height, result_coords (pointer to array of 2 c_uint32)
    stvision.find_line_bounds.restype = ctypes.c_uint32