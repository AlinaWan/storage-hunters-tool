import json
import os
import subprocess
import webbrowser
from datetime import datetime, timezone
from tkinter import filedialog
from typing import final as sealed

from core.config import Config
from core.constants import Constants
from services.file_watcher import FileWatcher
from utils.math_evaluator import MathEvaluator

config_watcher = FileWatcher()
current_config_path = None
config_data = None
recache_manager = None

evaluator = MathEvaluator({
    "SCREEN_WIDTH": Constants.SCREEN_WIDTH,
    "SCREEN_HEIGHT": Constants.SCREEN_HEIGHT
})

@sealed
class ConfigHandler:

    @staticmethod
    def apply_config(data):
        a = data["automation_settings"]
        Config.CLICK_COOLDOWN_MS = evaluator.evaluate(a["click_cooldown_ms"])
        Config.CLICK_COORDINATE = {
            "x": evaluator.evaluate(a["click_coordinate"]["x"]),
            "y": evaluator.evaluate(a["click_coordinate"]["y"]),
        }
        Config.SEARCH_REGION = {
            "top": evaluator.evaluate(a["search_region"]["top"]),
            "left": evaluator.evaluate(a["search_region"]["left"]),
            "width": evaluator.evaluate(a["search_region"]["width"]),
            "height": evaluator.evaluate(a["search_region"]["height"]),
        }
        Config.MAX_LINE_WIDTH_PX = evaluator.evaluate(a["max_line_width_px"])
        Config.LINE_BLIND_BUFFER_PX = evaluator.evaluate(a["line_blind_buffer_px"])
        Config.MIN_TARGET_WIDTH_PCT = float(evaluator.evaluate(a["min_target_width_pct"]))
        Config.MIN_TARGET_HEIGHT_PCT = float(evaluator.evaluate(a["min_target_height_pct"]))
        Config.TOOLTIP_MARKER_Y_OFFSET_PX = evaluator.evaluate(a["tooltip_marker_y_offset"])
        Config.USE_PREDICTIVE_COLLISION = evaluator.evaluate(a["use_predictive_collision"])

        h =data["hotkey_settings"]
        Config.TOGGLE_MOD = evaluator.evaluate(h["toggle"]["mod"])
        Config.TOGGLE_KEY = evaluator.evaluate(h["toggle"]["key"])
        Config.EXIT_MOD = evaluator.evaluate(h["exit"]["mod"])
        Config.EXIT_KEY = evaluator.evaluate(h["exit"]["key"])
        Config.MENU_MOD = evaluator.evaluate(h["menu"]["mod"])
        Config.MENU_KEY = evaluator.evaluate(h["menu"]["key"])
        Config.DEBUG_MOD = evaluator.evaluate(h["debug"]["mod"])
        Config.DEBUG_KEY = evaluator.evaluate(h["debug"]["key"])

    @staticmethod
    def _build_current_config():
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
                "click_cooldown_ms":        Config.CLICK_COOLDOWN_MS,
                "click_coordinate":         Config.CLICK_COORDINATE,
                "search_region":            Config.SEARCH_REGION,
                "max_line_width_px":        Config.MAX_LINE_WIDTH_PX,
                "line_blind_buffer_px":     Config.LINE_BLIND_BUFFER_PX,
                "min_target_width_pct":     Config.MIN_TARGET_WIDTH_PCT,
                "min_target_height_pct":    Config.MIN_TARGET_HEIGHT_PCT,
                "tooltip_marker_y_offset":  Config.TOOLTIP_MARKER_Y_OFFSET_PX,
                "use_predictive_collision": Config.USE_PREDICTIVE_COLLISION
            },
            "hotkey_settings": {
                "toggle": { "mod": Config.TOGGLE_MOD, "key": Config.TOGGLE_KEY },
                "exit":   { "mod": Config.EXIT_MOD,   "key": Config.EXIT_KEY   },
                "menu":   { "mod": Config.MENU_MOD,   "key": Config.MENU_KEY   },
                "debug":  { "mod": Config.DEBUG_MOD,  "key": Config.DEBUG_KEY  }
            }
        }

    @staticmethod
    def _reload_from_disk(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)

            ConfigHandler.apply_config(data)

            if recache_manager:
                recache_manager.trigger()

            print(f"[ConfigHandler::Reload] Live-reloaded: {os.path.basename(path)}")

        except Exception as e:
            print(f"[ConfigHandler::Reload] Reload error: {e}")

    @staticmethod
    def load_config():
        global current_config_path, config_data

        path = filedialog.askopenfilename(
            initialdir=Constants.SCRIPT_DIR,
            filetypes=[("JSON Config", "*.json")]
        )

        if not path:
            return

        # this prevents multiple threads from watching different files at once.
        config_watcher.stop()
        
        ConfigHandler._reload_from_disk(path)
        current_config_path = path

        # Start the watcher instance
        config_watcher.start(path, ConfigHandler._reload_from_disk)

    @staticmethod
    def edit_config():
        global current_config_path, config_data

        # 1. If no file is loaded, create one first
        if not current_config_path:
            timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
            default_name = f"Storage_Hunters_Tool_Config_{timestamp}.json"

            path = filedialog.asksaveasfilename(
                initialdir=Constants.SCRIPT_DIR,
                initialfile=default_name,
                defaultextension=".json",
                filetypes=[("JSON Config", "*.json")]
            )

            if not path:
                return # User cancelled the dialog

            # 2. Write the current script settings to the new file
            config = ConfigHandler._build_current_config()
            with open(path, "w") as f:
                json.dump(config, f, indent=4)

            # 3. Point the script to this new file
            current_config_path = path
            print(f"[ConfigHandler::Edit] Created and loaded config: {path}")

        # 4. Open the file (either the existing one or the one just created) in Notepad
        subprocess.Popen([Constants.TEXT_EDITOR_PATH, current_config_path])
        print(f"[ConfigHandler::Edit] Opened {current_config_path} with {Constants.TEXT_EDITOR_PATH}.")

        # 5. Ensure the watcher is running so edits are applied live
        if config_watcher._thread is None or not config_watcher._thread.is_alive():
            config_watcher.start(current_config_path, ConfigHandler._reload_from_disk)

    @staticmethod
    def open_help():
        github_url = f"{Constants.GITHUB_URL}#readme"
        webbrowser.open(github_url)

    @staticmethod
    def set_recache_manager(manager):
        global recache_manager
        recache_manager = manager