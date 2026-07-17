import json
import os
import subprocess
import webbrowser
from datetime import datetime, timezone
from tkinter import filedialog
from typing import final as sealed

from src.core.config import Config, ConfigDefaults
from src.core.constants import Constants
from src.dtos.config_runtime_state_dto import ConfigRuntimeStateDto
from src.utils.logger_mixin import LoggerMixin
from src.utils.math_evaluator import MathEvaluator

evaluator = MathEvaluator({
    "SCREEN_WIDTH": Constants.SCREEN_WIDTH,
    "SCREEN_HEIGHT": Constants.SCREEN_HEIGHT
})

@sealed
class ConfigHandler(LoggerMixin):
    def __init__(self, state: ConfigRuntimeStateDto):
        self.state = state
        self.evaluator = evaluator

    def _evaluate_or_default(self, expression, default):
        value = self.evaluator.evaluate(expression)
        return default if value is None else value

    def apply_config(self, data):
        defaults = ConfigDefaults.create_default_config_copy()

        a = data["automation_settings"]
        Config.CLICK_COOLDOWN_MS = self._evaluate_or_default(a["click_cooldown_ms"], defaults["CLICK_COOLDOWN_MS"])
        Config.CLICK_COORDINATE = {
            "x": self._evaluate_or_default(a["click_coordinate"]["x"], defaults["CLICK_COORDINATE"]["x"]),
            "y": self._evaluate_or_default(a["click_coordinate"]["y"], defaults["CLICK_COORDINATE"]["y"]),
        }
        Config.SEARCH_REGION = {
            "top": self._evaluate_or_default(a["search_region"]["top"], defaults["SEARCH_REGION"]["top"]),
            "left": self._evaluate_or_default(a["search_region"]["left"], defaults["SEARCH_REGION"]["left"]),
            "width": self._evaluate_or_default(a["search_region"]["width"], defaults["SEARCH_REGION"]["width"]),
            "height": self._evaluate_or_default(a["search_region"]["height"], defaults["SEARCH_REGION"]["height"]),
        }
        Config.USE_FULLSCREEN_OFFSET = self._evaluate_or_default(a["use_fullscreen_offset"], defaults["USE_FULLSCREEN_OFFSET"])
        Config.FULLSCREEN_Y_OFFSET = self._evaluate_or_default(a["fullscreen_y_offset"], defaults["FULLSCREEN_Y_OFFSET"])
        Config.MAX_LINE_WIDTH_PX = self._evaluate_or_default(a["max_line_width_px"], defaults["MAX_LINE_WIDTH_PX"])
        Config.LINE_BLIND_BUFFER_PX = self._evaluate_or_default(a["line_blind_buffer_px"], defaults["LINE_BLIND_BUFFER_PX"])
        Config.MIN_TARGET_WIDTH_PCT = float(self._evaluate_or_default(a["min_target_width_pct"], defaults["MIN_TARGET_WIDTH_PCT"]))
        Config.MIN_TARGET_HEIGHT_PCT = float(self._evaluate_or_default(a["min_target_height_pct"], defaults["MIN_TARGET_HEIGHT_PCT"]))
        Config.ALLOW_TARGET_BLEED = self._evaluate_or_default(a["allow_target_bleed"], defaults["ALLOW_TARGET_BLEED"])
        Config.TOOLTIP_MARKER_Y_OFFSET_PX = self._evaluate_or_default(a["tooltip_marker_y_offset"], defaults["TOOLTIP_MARKER_Y_OFFSET_PX"])
        Config.USE_PREDICTIVE_COLLISION = self._evaluate_or_default(a["use_predictive_collision"], defaults["USE_PREDICTIVE_COLLISION"])
        Config.PREDICTIVE_COLLISION_BUFFER = float(self._evaluate_or_default(a["predictive_collision_buffer"], defaults["PREDICTIVE_COLLISION_BUFFER"]))
        Config.MAX_PREDICTION_LATENCY_MS = float(self._evaluate_or_default(a["max_prediction_latency_ms"], defaults["MAX_PREDICTION_LATENCY_MS"]))

        h = data["hotkey_settings"]
        Config.TOGGLE_MOD = self._evaluate_or_default(h["toggle"]["mod"], defaults["TOGGLE_MOD"])
        Config.TOGGLE_KEY = self._evaluate_or_default(h["toggle"]["key"], defaults["TOGGLE_KEY"])
        Config.EXIT_MOD = self._evaluate_or_default(h["exit"]["mod"], defaults["EXIT_MOD"])
        Config.EXIT_KEY = self._evaluate_or_default(h["exit"]["key"], defaults["EXIT_KEY"])
        Config.MENU_MOD = self._evaluate_or_default(h["menu"]["mod"], defaults["MENU_MOD"])
        Config.MENU_KEY = self._evaluate_or_default(h["menu"]["key"], defaults["MENU_KEY"])
        Config.DEBUG_MOD = self._evaluate_or_default(h["debug"]["mod"], defaults["DEBUG_MOD"])
        Config.DEBUG_KEY = self._evaluate_or_default(h["debug"]["key"], defaults["DEBUG_KEY"])

        b = data["behavior_settings"]
        Config.ENABLE_DISCORD_RPC = self._evaluate_or_default(
            b["enable_discord_rpc"],
            defaults["ENABLE_DISCORD_RPC"]
        )

    def _nullify_value(value):
        if isinstance(value, dict):
            return {k: nullify(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [nullify(v) for v in value]
        return None

    def _build_current_config(self):
        return {
            "description": [
                "----------------- Storage Hunters Tool Configuration ----------------",
                " Feel free to add your own notes in the 'custom_info' section below! ",
                "                                                                     ",
                " You can write values as expressions based on screen dimensions with ",
                " variables SCREEN_WIDTH and SCREEN_HEIGHT (e.g., SCREEN_HEIGHT / 2). ",
                " Operators: +, -, *, /, //, %, **, +x, -x, &, |, ^, and parenthesis. ",
                "                                                                     ",
                " Hotkeys can be written as either hexadecimal or decimal. The        ",
                " bitwise OR (|) operator is particularly useful for bitmasking.      ",
                "---------------------------------------------------------------------"
                ],
            "metadata": {
                "custom_info": {
                    "author":   "",
                    "trophies": "",
                    "garage":   ""
                },
                "app_info": {
                    "version": "1.0.0",
                    "schema":  1,
                    "created": datetime.now(timezone.utc).isoformat(),
                }
            },
            "automation_settings": {
                "click_cooldown_ms":           Config.CLICK_COOLDOWN_MS,
                "click_coordinate":            Config.CLICK_COORDINATE,
                "search_region":               Config.SEARCH_REGION,
                "use_fullscreen_offset":       Config.USE_FULLSCREEN_OFFSET,
                "fullscreen_y_offset":         Config.FULLSCREEN_Y_OFFSET,
                "max_line_width_px":           Config.MAX_LINE_WIDTH_PX,
                "line_blind_buffer_px":        Config.LINE_BLIND_BUFFER_PX,
                "min_target_width_pct":        Config.MIN_TARGET_WIDTH_PCT,
                "min_target_height_pct":       Config.MIN_TARGET_HEIGHT_PCT,
                "allow_target_bleed":          Config.ALLOW_TARGET_BLEED,
                "tooltip_marker_y_offset":     Config.TOOLTIP_MARKER_Y_OFFSET_PX,
                "use_predictive_collision":    Config.USE_PREDICTIVE_COLLISION,
                "predictive_collision_buffer": Config.PREDICTIVE_COLLISION_BUFFER,
                "max_prediction_latency_ms":   Config.MAX_PREDICTION_LATENCY_MS
            },
            "hotkey_settings": {
                "toggle": { "mod": Config.TOGGLE_MOD, "key": Config.TOGGLE_KEY },
                "exit":   { "mod": Config.EXIT_MOD,   "key": Config.EXIT_KEY   },
                "menu":   { "mod": Config.MENU_MOD,   "key": Config.MENU_KEY },
                "debug":  { "mod": Config.DEBUG_MOD,  "key": Config.DEBUG_KEY  }
            },
            "behavior_settings": {
                "enable_discord_rpc": Config.ENABLE_DISCORD_RPC
            }
        }

    def _reload_from_disk(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)

            self.apply_config(data)

            if self.state.recache_manager:
                self.state.recache_manager.trigger()

            self.logger.info(f"Live-reloaded: {os.path.basename(path)}")

        except Exception as _:
            self.logger.exception(f"Reload error for {os.path.basename(path)}")

    def load_config(self, path: str | None = None):
        # If no path was passed (clicked via UI button), open the file dialog
        # else, the file was drag-dropped and the path is passed
        if not path:
            path = filedialog.askopenfilename(
                initialdir=Constants.SCRIPT_DIR,
                filetypes=[("JSON Config", "*.json")]
            )

        if not path:
            return

        self.state.config_watcher.stop()
        
        self._reload_from_disk(path)
        self.state.current_config_path = path

        self.state.config_watcher.start(path, self._reload_from_disk)

    def edit_config(self):
        if not self.state.current_config_path:
            timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
            default_name = f"Storage_Hunters_Tool_Config_{timestamp}.json"

            path = filedialog.asksaveasfilename(
                initialdir=Constants.SCRIPT_DIR,
                initialfile=default_name,
                defaultextension=".json",
                filetypes=[("JSON Config", "*.json")]
            )

            if not path:
                return

            config = self._build_current_config()
            with open(path, "w") as f:
                json.dump(config, f, indent=4)

            self.state.current_config_path = path
            self.logger.info(f"Created and loaded config: {path}")

        subprocess.Popen([Constants.TEXT_EDITOR_PATH, self.state.current_config_path])
        self.logger.info(f"Opened {self.state.current_config_path} with {Constants.TEXT_EDITOR_PATH}.")

        if self.state.config_watcher._thread is None or not self.state.config_watcher._thread.is_alive():
            self.state.config_watcher.start(self.state.current_config_path, self._reload_from_disk)

    def open_help(self):
        github_url = f"{Constants.GITHUB_URL}#readme"
        webbrowser.open(github_url)

    def set_recache_manager(self, manager):
        self.state.recache_manager = manager