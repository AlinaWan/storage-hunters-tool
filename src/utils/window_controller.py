from enum import Enum, auto
from typing import final as sealed

from src.core.native_methods import NativeMethods

class FocusWindowResult(Enum):
    SUCCESS = auto()
    NO_VISIBLE_WINDOW = auto()

@sealed
class WindowController():
    @staticmethod
    def focus_window(pid: int, hwnd: int) -> FocusWindowResult:
        if hwnd is None:
            return FocusWindowResult.NO_VISIBLE_WINDOW

        NativeMethods.force_focus_window(hwnd)
        return FocusWindowResult.SUCCESS