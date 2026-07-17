from copy import deepcopy
from typing import final as sealed

from src.core.constants import Constants

@sealed
class Config:

    # Automation
    CLICK_COOLDOWN_MS = 250
    CLICK_COORDINATE = {"x": int(Constants.SCREEN_WIDTH / 2),
                        "y": int(Constants.SCREEN_HEIGHT * (860 / 1080))}

    if Constants.SCREEN_WIDTH * 9 == Constants.SCREEN_HEIGHT * 16:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (752 / 1080)),
                         "left":   int(Constants.SCREEN_WIDTH  * (614 / 1920)),
                         "width":  int(Constants.SCREEN_WIDTH  * (692 / 1920)),
                         "height": int(Constants.SCREEN_HEIGHT * (57 / 1080))}
    elif Constants.SCREEN_WIDTH * 10 == Constants.SCREEN_HEIGHT * 16:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (748 / 1050)),
                         "left":   int(Constants.SCREEN_WIDTH  * (538 / 1680)),
                         "width":  int(Constants.SCREEN_WIDTH  * (604 / 1680)),
                         "height": int(Constants.SCREEN_HEIGHT * (50 / 1050))}
    elif Constants.SCREEN_WIDTH * 16 == Constants.SCREEN_HEIGHT * 25:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (732 / 1024)),
                         "left":   int(Constants.SCREEN_WIDTH  * (512 / 1600)),
                         "width":  int(Constants.SCREEN_WIDTH  * (576 / 1600)),
                         "height": int(Constants.SCREEN_HEIGHT * (48 / 1024))}
    elif Constants.SCREEN_WIDTH * 3 == Constants.SCREEN_HEIGHT * 4:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (798 / 1080)),
                         "left":   int(Constants.SCREEN_WIDTH  * (461 / 1440)),
                         "width":  int(Constants.SCREEN_WIDTH  * (518 / 1440)),
                         "height": int(Constants.SCREEN_HEIGHT * (43 / 1080))}
    elif Constants.SCREEN_WIDTH * 35 == Constants.SCREEN_HEIGHT * 48:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (775 / 1050)),
                         "left":   int(Constants.SCREEN_WIDTH  * (448 / 1440)),
                         "width":  int(Constants.SCREEN_WIDTH  * (504 / 1440)),
                         "height": int(Constants.SCREEN_HEIGHT * (41 / 1050))}
    elif Constants.SCREEN_WIDTH * 384 == Constants.SCREEN_HEIGHT * 683:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (524 / 768)),
                         "left":   int(Constants.SCREEN_WIDTH  * (437 / 1366)),
                         "width":  int(Constants.SCREEN_WIDTH  * (492 / 1366)),
                         "height": int(Constants.SCREEN_HEIGHT * (41 / 768))}
    elif Constants.SCREEN_WIDTH * 48 == Constants.SCREEN_HEIGHT * 85:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (525 / 768)),
                         "left":   int(Constants.SCREEN_WIDTH  * (435 / 1360)),
                         "width":  int(Constants.SCREEN_WIDTH  * (490 / 1360)),
                         "height": int(Constants.SCREEN_HEIGHT * (40 / 768))}
    elif Constants.SCREEN_WIDTH * 4 == Constants.SCREEN_HEIGHT * 5:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (763 / 1024)),
                         "left":   int(Constants.SCREEN_WIDTH  * (410 / 1280)),
                         "width":  int(Constants.SCREEN_WIDTH  * (460 / 1280)),
                         "height": int(Constants.SCREEN_HEIGHT * (38 / 1024))}
    elif Constants.SCREEN_WIDTH * 3 == Constants.SCREEN_HEIGHT * 5:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (533 / 768)),
                         "left":   int(Constants.SCREEN_WIDTH  * (410 / 1280)),
                         "width":  int(Constants.SCREEN_WIDTH  * (460 / 1280)),
                         "height": int(Constants.SCREEN_HEIGHT * (38 / 768))}
    elif Constants.SCREEN_WIDTH * 15 == Constants.SCREEN_HEIGHT * 32:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (381 / 600)),
                         "left":   int(Constants.SCREEN_WIDTH  * (410 / 1280)),
                         "width":  int(Constants.SCREEN_WIDTH  * (460 / 1280)),
                         "height": int(Constants.SCREEN_HEIGHT * (38 / 600))}
    else:
        SEARCH_REGION = {"top":    int(Constants.SCREEN_HEIGHT * (752 / 1080)),
                         "left":   int(Constants.SCREEN_WIDTH  * (614 / 1920)),
                         "width":  int(Constants.SCREEN_WIDTH  * (692 / 1920)),
                         "height": int(Constants.SCREEN_HEIGHT * (57 / 1080))}

    USE_FULLSCREEN_OFFSET = False
    FULLSCREEN_Y_OFFSET = int(Constants.SCREEN_HEIGHT * (40 / 1080))
    MAX_LINE_WIDTH_PX = int(Constants.SCREEN_WIDTH * (20 / 1920))
    LINE_BLIND_BUFFER_PX = int(Constants.SCREEN_WIDTH * (10 / 1920))
    MIN_TARGET_WIDTH_PCT = 5.0
    MIN_TARGET_HEIGHT_PCT = 90.0
    ALLOW_TARGET_BLEED = True
    TOOLTIP_MARKER_Y_OFFSET_PX = int(Constants.SCREEN_HEIGHT * (20 / 1080))
    USE_PREDICTIVE_COLLISION = False
    PREDICTIVE_COLLISION_BUFFER = 0.1
    MAX_PREDICTION_LATENCY_MS = 30.0

    # Behavior
    ENABLE_DISCORD_RPC = False

    # Hotkey
    TOGGLE_MOD, TOGGLE_KEY = 0, 117                  # F6 (0, 0x75)
    EXIT_MOD, EXIT_KEY = 4, 27                       # Shift + Esc (0x0004, 0x1B)
    MENU_MOD, MENU_KEY = 2, 121                      # Ctrl + F10 (0x0002, 0x79)
    CANCEL_SHUTDOWN_MOD, CANCEL_SHUTDOWN_KEY = 6, 88 # Ctrl + Shift + X (0x0002 | 0x0004, 0x58)
    DEBUG_MOD, DEBUG_KEY = 0, 118                    # F7 (0, 0x76)

@sealed
class ConfigDefaults:
    @staticmethod
    def create_default_config_copy():
        """Returns a fresh deepcopy of the default configuration values."""
        return deepcopy(_DEFAULT_CONFIG_STATE)

# Make a copy of the default state to handle null -> use default
_DEFAULT_CONFIG_STATE = {
    key: value
    for key, value in Config.__dict__.items()
    if key.isupper()
}