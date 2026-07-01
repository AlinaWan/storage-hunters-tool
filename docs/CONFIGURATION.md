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
| `USE_FULLSCREEN_OFFSET` | A boolean toggle to manually enable vertical adjustments for fullscreen use, which shifts both the click coordinates and the search region. |
| `FULLSCREEN_Y_OFFSET` | The vertical displacement value in pixels applied to use if `USE_FULLSCREEN_OFFSET` is `True`. A positive value moves the click coordinate and search region down. |
| `MAX_LINE_WIDTH_PX` | The maximum allowable pixel width for the moving indicator line, used as a structural threshold to distinguish the valid tracking line from background noise or larger UI elements. |
| `LINE_BLIND_BUFFER_PX` | The pixel radius defining a blind mask buffer to both sides of the tracking line to eliminate self-detection interference. |
| `MIN_TARGET_WIDTH_PCT` | The minimum required horizontal span of the target area, evaluated as a precise percentage of the total search region width. |
| `MIN_TARGET_HEIGHT_PCT` | The minimum required vertical coverage of the target area, evaluated as a precise percentage of the total search region height. |
| `ALLOW_TARGET_BLEED` | A boolean toggle that allows the tracking line to merge with and expand the target area's bounding box upon physical contact. This is a side-effect which may improve accuracy by causing the leading edge of the tracking line to trigger a click upon contact with the target area, allowing the actual hit to land cleanly within the zone under normal latency. Turning this `False` to stop the tracking line from expanding the target area is only recommended for ultra-low latency systems (sub-10ms) experiencing early misfires. |
| `TOOLTIP_MARKER_Y_OFFSET_PX` | The Y-axis offset in pixels to move the tooltip markers above or below the detected tracking line and target area. A positive value moves the tooltip markers up. |
| `USE_PREDICTIVE_COLLISION` | A boolean toggle that enables or disables lead-prediction algorithms, dictating whether the engine should click dynamically ahead of the line's real-time position using estimated latency math. |
| `PREDICTIVE_COLLISION_BUFFER` | A float value (from `0.0` to `1.0`) representing the percentage of the target area's total width used as an entry-side padding during lead-prediction. This shifts the target inward to absorb normal variations in latency. |
| `MAX_PREDICTION_LATENCY_MS` | A hard upper limit (in milliseconds) that clamps the lead-prediction lookahead math, which may prevent the simulated click trajectory from undershooting the target resolution bounds. |