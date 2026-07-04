from typing import Tuple, Optional

import numpy as np

from src.core.interfaces import IFrameProvider

class PythonMssFrameProvider(IFrameProvider):
    def __init__(self) -> None:
        import mss
        self._sct = mss.mss()

    def grab(self, region: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        monitor = {
            "left": region[0],
            "top": region[1],
            "width": region[2] - region[0],
            "height": region[3] - region[1]
        }
        sct_img = self._sct.grab(monitor)
        return np.array(sct_img)

    def close(self) -> None:
        if hasattr(self, '_sct'):
            self._sct.close()