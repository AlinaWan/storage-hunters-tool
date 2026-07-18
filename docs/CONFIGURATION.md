# 🛠️ Configuration Guide

> [!TIP]
> You can find premade KC Config Suite configurations in the [`configs`](../configs/) directory.
>
> Made a configuration that works well for your setup? Share it in the [Riri's Tools Discord server](https://discord.gg/EFDsph8EJF) so others can try it too!

All adjustable parameters can be stored in a human-readable `.json` file. This allows users to easily export, share, and import configurations without needing to modify the source code.

These configuration files can be managed through the in-app menu (<kbd>Ctrl</kbd> + <kbd>F10</kbd>), providing a user-friendly interface for customization and optimization based on individual hardware capabilities and display setups.

## ⚙️ Constants Breakdown

Adjust these values within your `.json` config to align with your hardware's performance profile.

### 1. Intersection Automation (Main Interaction)
| Constant | Function |
| :--- | :--- |
| `CLICK_COOLDOWN_MS` | The minimum cooling period (in milliseconds) required between consecutive mouse click triggers to prevent spamming. |
| `CLICK_COORDINATE` | The absolute screen position coordinate dictionary `{"x", "y"}` where the click action will be dispatched. |
| `SEARCH_REGION` | The localized bounding box dictionary defining the vertical/horizontal pixel coordinates and dimensions of the processing capture zone. **IMPORTANT: If you use any one of the following aspect ratios, you should NOT need to change this regardless of your resolution: 16:9, 16:10, 25:16, 4:3, 48:35, 683:384, 85:48, 5:4, 5:3, 32:15.** Only change this if you use a scale other than 100% or the search area is still incorrect after using the application. |
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

### 2. Behavior Preferences
| Constant | Function |
| :--- | :--- |
| `ENABLE_DISCORD_RPC` | A boolean toggle to enable or disable Discord Rich Presence, which broadcasts the current status through a secure IPC queuing method via FIFO. |

## 🧮 Expression Support

> [!IMPORTANT]
> Any expression must be written as a **JSON string** by wrapping it in quotes.
>
> ✅ Correct:
> ```json
> "CLICK_COORDINATE": "SCREEN_WIDTH // 2"
> ```
>
> ❌ Incorrect:
> ```json
> "CLICK_COORDINATE": SCREEN_WIDTH // 2
> ```

Numeric configuration values also support mathematical expressions. Expressions are evaluated with the whitelisted operations, functions, and variables listed below.

### Operators

| Operator | Description | Example |
| :--- | :--- | :--- |
| `+` | Addition | `100 + 50` |
| `-` | Subtraction | `1920 - 100` |
| `*` | Multiplication | `10 * 2` |
| `/` | Division | `1920 / 2` |
| `//` | Floor division | `100 // 3` |
| `%` | Modulo (remainder) | `10 % 3` |
| `**` | Exponentiation | `2 ** 8` |
| `+x` | Positive value | `+100` |
| `-x` | Negative value | `-50` |
| `\|` | Bitwise OR (integers only) | `4 | 2` |
| `&` | Bitwise AND (integers only) | `6 & 3` |
| `^` | Bitwise XOR (integers only) | `5 ^ 3` |

### Functions

| Function | Description | Example |
| :--- | :--- | :--- |
| `int(x)` | Converts a number to an integer by truncating the decimal portion | `int(10.8)` → `10` |
| `round(x)` | Rounds a number to the nearest integer using banker's rounding | `round(10.8)` → `11` |
| `min(x, ...)` | Returns the smallest value from the provided numbers | `min(100, 50, 75)` → `50` |
| `max(x, ...)` | Returns the largest value from the provided numbers | `max(100, 50, 75)` → `100` |
| `abs(x)` | Returns the absolute value of a number | `abs(-50)` → `50` |

### Variables

| Variable | Description | Example |
| :--- | :--- | :--- |
| `SCREEN_WIDTH` | The horizontal dimension (in pixels) of **the current user's** primary monitor | `SCREEN_WIDTH // 2` |
| `SCREEN_HEIGHT` | The vertical dimension (in pixels) of **the current user's** primary monitor | `SCREEN_HEIGHT // 2` |

### Fallback Behavior

If an value is `null` or an expression is invalid, the configuration handler will ignore the provided value and use the default configuration value instead.

Examples:

```json
{
  "CLICK_COOLDOWN_MS": null,
  "MAX_LINE_WIDTH_PX": "abcde"
}
```

> [!TIP]
> It is recommended to use `null` for values like `CLICK_COORDINATE` and `SEARCH_REGION` if you intend to share or make portable your configuration,
> as most pixel-based configuration values automatically adjust to the current user's screen size by default.