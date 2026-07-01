import json
import os
import subprocess
import webbrowser
from datetime import datetime, timezone
from tkinter import filedialog
from typing import final as sealed

from core.config import Config
from core.constants import Constants
from dtos.config_runtime_state_dto import ConfigRuntimeStateDto
from utils.math_evaluator import MathEvaluator

evaluator = MathEvaluator({
    "SCREEN_WIDTH": Constants.SCREEN_WIDTH,
    "SCREEN_HEIGHT": Constants.SCREEN_HEIGHT
})

@sealed
class ConfigHandler:
    def __init__(self, state: ConfigRuntimeStateDto):
        self.state = state
        self.evaluator = evaluator

    def apply_config(self, data):
        a = data["automation_settings"]
        Config.CLICK_COOLDOWN_MS = self.evaluator.evaluate(a["click_cooldown_ms"])
        Config.CLICK_COORDINATE = {
            "x": self.evaluator.evaluate(a["click_coordinate"]["x"]),
            "y": self.evaluator.evaluate(a["click_coordinate"]["y"]),
        }
        Config.SEARCH_REGION = {
            "top": self.evaluator.evaluate(a["search_region"]["top"]),
            "left": self.evaluator.evaluate(a["search_region"]["left"]),
            "width": self.evaluator.evaluate(a["search_region"]["width"]),
            "height": self.evaluator.evaluate(a["search_region"]["height"]),
        }
        Config.USE_FULLSCREEN_OFFSET = self.evaluator.evaluate(a["use_fullscreen_offset"])
        Config.FULLSCREEN_Y_OFFSET = self.evaluator.evaluate(a["fullscreen_y_offset"])
        Config.MAX_LINE_WIDTH_PX = self.evaluator.evaluate(a["max_line_width_px"])
        Config.LINE_BLIND_BUFFER_PX = self.evaluator.evaluate(a["line_blind_buffer_px"])
        Config.MIN_TARGET_WIDTH_PCT = float(self.evaluator.evaluate(a["min_target_width_pct"]))
        Config.MIN_TARGET_HEIGHT_PCT = float(self.evaluator.evaluate(a["min_target_height_pct"]))
        Config.ALLOW_TARGET_BLEED = self.evaluator.evaluate(a["allow_target_bleed"])
        Config.TOOLTIP_MARKER_Y_OFFSET_PX = self.evaluator.evaluate(a["tooltip_marker_y_offset"])
        Config.USE_PREDICTIVE_COLLISION = self.evaluator.evaluate(a["use_predictive_collision"])
        Config.PREDICTIVE_COLLISION_BUFFER = float(self.evaluator.evaluate(a["predictive_collision_buffer"]))
        Config.MAX_PREDICTION_LATENCY_MS = float(self.evaluator.evaluate(a["max_prediction_latency_ms"]))

        h = data["hotkey_settings"]
        Config.TOGGLE_MOD = self.evaluator.evaluate(h["toggle"]["mod"])
        Config.TOGGLE_KEY = self.evaluator.evaluate(h["toggle"]["key"])
        Config.EXIT_MOD = self.evaluator.evaluate(h["exit"]["mod"])
        Config.EXIT_KEY = self.evaluator.evaluate(h["exit"]["key"])
        Config.MENU_MOD = self.evaluator.evaluate(h["menu"]["mod"])
        Config.MENU_KEY = self.evaluator.evaluate(h["menu"]["key"])
        Config.DEBUG_MOD = self.evaluator.evaluate(h["debug"]["mod"])
        Config.DEBUG_KEY = self.evaluator.evaluate(h["debug"]["key"])

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
                "menu":   { "menu_mod": Config.MENU_MOD, "key": Config.MENU_KEY },
                "debug":  { "mod": Config.DEBUG_MOD,  "key": Config.DEBUG_KEY  }
            }
        }

    def _reload_from_disk(self, path):
        try:
            with open(path, "r") as f:
                data = json.load(f)

            self.apply_config(data)

            if self.state.recache_manager:
                self.state.recache_manager.trigger()

            print(f"[ConfigHandler::Reload] Live-reloaded: {os.path.basename(path)}")

        except Exception as e:
            print(f"[ConfigHandler::Reload] Reload error: {e}")

    def load_config(self):
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
            print(f"[ConfigHandler::Edit] Created and loaded config: {path}")

        subprocess.Popen([Constants.TEXT_EDITOR_PATH, self.state.current_config_path])
        print(f"[ConfigHandler::Edit] Opened {self.state.current_config_path} with {Constants.TEXT_EDITOR_PATH}.")

        if self.state.config_watcher._thread is None or not self.state.config_watcher._thread.is_alive():
            self.state.config_watcher.start(self.state.current_config_path, self._reload_from_disk)

    def open_help(self):
        github_url = f"{Constants.GITHUB_URL}#readme"
        webbrowser.open(github_url)

    def set_recache_manager(self, manager):
        self.state.recache_manager = manager