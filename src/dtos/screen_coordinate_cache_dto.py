from typing import Dict as Dictionary, final as sealed

@sealed
class ScreenCoordinateCacheDto:
    def __init__(self):

        self.search_region: Dictionary[str, int] = {
            "left": 0,
            "top": 0,
            "width": 0,
            "height": 0
        }

        self.click_coordinate: Dictionary[str, int] = {
            "x": 0,
            "y": 0
        }