from typing import final as sealed

from core.constants import Constants

@sealed
class Config:

    # Automation
    CLICK_COOLDOWN_MS = 250
    CLICK_COORDINATE = {"x": int(Constants.SCREEN_WIDTH  * (960 / 1920)),
                        "y": int(Constants.SCREEN_HEIGHT * (860 / 1080))}
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