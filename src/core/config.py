from typing import final as sealed

from core.constants import Constants

@sealed
class Config:

    CLICK_COOLDOWN_MS = 100
    CLICK_COORDINATE = {"x": 940, "y": 860}
    SEARCH_REGION = {"top": 752, "left": 614, "width": 692, "height": 57}
    BLIND_ZONE_RADIUS = 10