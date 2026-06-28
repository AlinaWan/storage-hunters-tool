# 🛠️ Configuration Guide

All adjustable parameters can be stored in a human-readable `.json` file. This allows users to easily export, share, and import configurations without needing to modify the source code.

These configuration files can be managed through the in-app menu (<kbd>Ctrl</kbd> + <kbd>F10</kbd>), providing a user-friendly interface for customization and optimization based on individual hardware capabilities and display setups.

## ⚙️ Constants Breakdown

Adjust these values within your `.json` config to align with your hardware's performance profile.

### 1. Slider Automation (Main Interaction)
| Constant | Function |
| :--- | :--- |
| `CONFIDENCE_THRESHOLD` | The minimum normalized correlation coefficient (`0.0` to `1.0`) required for a match. |
| `ROTATION_STEP` | The angular increment used to generate the rotated template cache. |
| `DRAG_STEP` | The scalar magnitude of the corrective mouse displacement applied after engagement. |
| `COOLDOWN_MS` | The minimum delay between successive corrective drag actions. |
| `LOCK_DURATION_MS` | The required temporal persistence (in milliseconds) before the tool engages the target. |
| `DOWNSCALE_FACTOR` | Scaling ratio applied to the search domain to reduce computational load (`O(n²)` reduction). |
| `BOUNDARY_MARGIN` | Pixel buffer allowing the drag destination to exist outside the ROI before invalidation. |
| `MINIGAME_TIMEOUT_MS` | Duration a slider has not been detected before the system infers the minigame has ended. |

### 2. Meter Automation (Swing Release)
| Constant | Function |
| :--- | :--- |
| `AUTO_RELEASE_ENABLED` | Toggles the calibration and execution of the automated meter-release system. |
| `AUTO_RELEASE_TOLERANCE` | The maximum per-channel RGB deviation allowed when validating pixel matches. |
| `AUTO_RELEASE_CONFIDENCE` | The normalized correlation threshold required for meter template calibration. |
| `AUTO_RELEASE_Y_OFFSET` | The vertical pixel shift that moves the sampling region downward from the detected meter anchor point. |
| `SEARCH_DEPTH` | The number of vertical pixels scanned downward from the starting point when evaluating the meter column. |

### 3. Routine Automation (Traversal & Swing Execution)
| Constant | Function |
| :--- | :--- |
| `AUTO_ROUTINE_ENABLED` | Enables the autonomous walk-and-swing routine (implicitly forces `AUTO_RELEASE_ENABLED`). |
| `AUTO_ROUTINE_PATTERN` | The ordered movement sequence executed between swing attempts. |
| `AUTO_ROUTINE_WALK_TIME_MS` | Duration each movement key is held during routine traversal. |
| `AUTO_ROUTINE_LMB_TIMEOUT_MS` | Maximum duration the routine will hold LMB awaiting a minigame before aborting the current cycle. |

### 4. Behavior Preferences
| Constant | Function |
| :--- | :--- |
| `DISCORD_WEBHOOK_ENABLED` | Global toggle for Discord notifications. |
| `DISCORD_WEBHOOK_URL` | Your private Discord Webhook URL to send the notifications. |
| `DISCORD_WEBHOOK_INTERVAL` | How often (in number of catches) the tool sends a "Total Caught" status update. |
| `DISCORD_WEBHOOK_RARITY_TOLERANCE` | The maximum per-channel RGB deviation allowed when validating pixel matches for rarity colors. |
| `DISCORD_WEBHOOK_RARITY_ALERTS` | A map of bee rarities (e.g., `mythic`, `secret`) that will trigger an immediate notification with a screenshot of the entire screen. |
| `EXIT_ON_ROBLOX_DISCONNECT` | Shuts down the program if the current Roblox instance indicates a disconnect. |
| `SHUTDOWN_ON_ROBLOX_DISCONNECT` | Sends the shutdown signal with a 15 second timer if the current Roblox instance indicates a disconnect. |
| `EXIT_ON_ROBLOX_KILL` | Shuts down the program if the current Roblox process ID is killed. |
| `SHUTDOWN_ON_ROBLOX_KILL` | Sends the shutdown signal with a 15 second timer if the current Roblox process ID is killed. |

> [!CAUTION]
> **Do not share your configuration files if they contain a `DISCORD_WEBHOOK_URL`.**
>
> Anyone with this URL can send messages to your Discord server or potentially delete the webhook. Treat this URL like a password.

---

### Template Fidelity
Templates based on a 1920x1080 resolution are provided as a baseline, but users may need to capture custom templates if their display configuration differs significantly. Although manual pixel coordinate entry is not required, the tool's performance is highly dependent on the quality of the template matches.

* **`target.png`**: The inner part of the hexagon slider. Encompass the entire white arrow and do not include the background. This one doesn't need to be pixel-perfect.
* **`meter.png`**: The entire completely filled green meter including the dark-green outline. You may need to take the screenshot into Adobe Photoshop or Photopea to finely crop the meter.
