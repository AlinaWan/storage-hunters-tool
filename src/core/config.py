from typing import final as sealed

from core.constants import Constants

@sealed
class Config:

    CLICK_COOLDOWN_MS = 250
    CLICK_COORDINATE = {"x": 960, "y": 860}
    SEARCH_REGION = {"top": 752, "left": 614, "width": 692, "height": 57}
    MAX_LINE_WIDTH_PX = 20
    LINE_BLIND_BUFFER_PX = 10
    MIN_TARGET_WIDTH_PCT = 5.0
    MIN_TARGET_HEIGHT_PCT = 90.0
    TOOLTIP_MARKER_Y_OFFSET_PX = int(Constants.SCREEN_HEIGHT * (20 / 1080))
    USE_PREDICTIVE_COLLISION = True

    # --- Hotkey Preference ---
    TOGGLE_MOD, TOGGLE_KEY = 0, 117                  # F6 (0, 0x75)
    EXIT_MOD, EXIT_KEY = 4, 27                       # Shift + Esc (0x0004, 0x1B)
    MENU_MOD, MENU_KEY = 2, 121                      # Ctrl + F10 (0x0002, 0x79)
    CANCEL_SHUTDOWN_MOD, CANCEL_SHUTDOWN_KEY = 6, 88 # Ctrl + Shift + X (0x0002 | 0x0004, 0x58)
    DEBUG_MOD, DEBUG_KEY = 0, 118                    # F7 (0, 0x76)