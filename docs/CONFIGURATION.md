# 🛠️ Configuration Guide

All adjustable parameters can be stored in a human-readable `.json` file. This allows users to easily export, share, and import configurations without needing to modify the source code.

These configuration files can be managed through the in-app menu (<kbd>Ctrl</kbd> + <kbd>F10</kbd>), providing a user-friendly interface for customization and optimization based on individual hardware capabilities and display setups.

## ⚙️ Constants Breakdown

Adjust these values within your `.json` config to align with your hardware's performance profile.

### 1. Intersection Automation (Main Interaction)
| Constant | Function |
| :--- | :--- |
| `CLICK_COOLDOWN_MS` | The minimum cooling period (in milliseconds) required between consecutive mouse click triggers to prevent spamming. |
| `CLICK_COORDINATE` | The absolute screen position coordinate dictionary `{"x", "y"}` where the click action will be dispatched. |
| `SEARCH_REGION` | The localized bounding box dictionary defining the vertical/horizontal pixel coordinates and dimensions of the processing capture zone. |
| `MAX_LINE_WIDTH_PX` | The maximum horizontal span of an area to be detected as the tracking line. |
| `LINE_BLIND_BUFFER_PX` | The pixel radius defining a blind mask buffer to both sides of the tracking line to eliminate self-detection interference. |
| `MIN_TARGET_WIDTH_PCT` | The minimum required horizontal span of the target area, evaluated as a precise percentage of the total search region width. |
| `MIN_TARGET_HEIGHT_PCT` | The minimum required vertical coverage of the target area, evaluated as a precise percentage of the total search region height. |
| `TOOLTIP_MARKER_Y_OFFSET_PX` | The Y-axis offset in pixels to move the tooltip markers above or below the detected tracking line and target area. |