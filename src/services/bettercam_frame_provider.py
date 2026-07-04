from typing import Tuple, Optional

import numpy as np

from src.core.interfaces import IFrameProvider

class BetterCamFrameProvider(IFrameProvider):
    def __init__(self) -> None:
        import bettercam
        self._camera = bettercam.create(output_color="BGRA")

    def grab(self, region: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        return self._camera.grab(region=region)

    def close(self) -> None:
        if hasattr(self, '_camera'):
            del self._camera