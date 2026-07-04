import ctypes
import os
from typing import Tuple, Optional
import numpy as np

from src.core.interfaces import IFrameProvider

class DxgiFrameProvider(IFrameProvider):
    def __init__(self, dll_path: str = "src\\native\\DxgiCapture.dll") -> None:
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"Could not find DXGI DLL at {dll_path}")
            
        self._dll = ctypes.CDLL(dll_path)
        
        self._dll.InitContext.argtypes = []
        self._dll.InitContext.restype = ctypes.c_void_p
        
        self._dll.GrabFramePointer.argtypes = [
            ctypes.c_void_p,  # ctx
            ctypes.c_int,     # left
            ctypes.c_int,     # top
            ctypes.c_int,     # right
            ctypes.c_int,     # bottom
            ctypes.POINTER(ctypes.c_int) # outRowPitch
        ]
        self._dll.GrabFramePointer.restype = ctypes.POINTER(ctypes.c_ubyte)
        
        self._dll.UnlockFramePointer.argtypes = [ctypes.c_void_p]
        self._dll.UnlockFramePointer.restype = None
        
        self._dll.CloseContext.argtypes = [ctypes.c_void_p]
        self._dll.CloseContext.restype = None

        self._ctx = self._dll.InitContext()
        if not self._ctx:
            raise RuntimeError("Failed to initialize DXGI Pipeline context.")

        self._is_locked = False

    def grab(self, region: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        # If a previous frame is still mapped, unmap it before acquiring the next
        if self._is_locked:
            self._dll.UnlockFramePointer(self._ctx)
            self._is_locked = False

        left, top, right, bottom = region
        width = right - left
        height = bottom - top
        row_pitch = ctypes.c_int(0)

        # Grab direct memory pointer from C++ GPU staging map
        data_ptr = self._dll.GrabFramePointer(self._ctx, left, top, right, bottom, ctypes.byref(row_pitch))
        
        if not data_ptr:
            return None
            
        self._is_locked = True

        buffer_size = row_pitch.value * height

        buffer = np.ctypeslib.as_array(
            ctypes.cast(data_ptr, ctypes.POINTER(ctypes.c_uint8)),
            shape=(buffer_size,),
        )

        frame = np.ndarray(
            shape=(height, width, 4),
            dtype=np.uint8,
            buffer=buffer,
            strides=(row_pitch.value, 4, 1),
        )

        return frame

    def close(self) -> None:
        if hasattr(self, '_ctx') and self._ctx:
            if self._is_locked:
                self._dll.UnlockFramePointer(self._ctx)
                self._is_locked = False
            self._dll.CloseContext(self._ctx)
            self._ctx = None