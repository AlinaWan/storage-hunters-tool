from typing import final as sealed

from core.constants import Constants

@sealed
class Config:

    CLICK_COOLDOWN_MS = 100
    CLICK_COORDINATE = {"x": 960, "y": 860}
    SEARCH_REGION = {"top": 752, "left": 614, "width": 692, "height": 57}
    BLIND_ZONE_RADIUS = 10

    # --- Hotkey Preference ---
    TOGGLE_MOD, TOGGLE_KEY = 0, 117                  # F6 (0, 0x75)
    EXIT_MOD, EXIT_KEY = 4, 27                       # Shift + Esc (0x0004, 0x1B)
    MENU_MOD, MENU_KEY = 2, 121                      # Ctrl + F10 (0x0002, 0x79)
    CANCEL_SHUTDOWN_MOD, CANCEL_SHUTDOWN_KEY = 6, 88 # Ctrl + Shift + X (0x0002 | 0x0004, 0x58)