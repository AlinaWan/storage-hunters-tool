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
        s = data["slider_settings"]
        Config.CONFIDENCE_THRESHOLD = evaluator.evaluate(s["confidence_threshold"])
        Config.ROTATION_STEP = evaluator.evaluate(s["rotation_step"])
        Config.DRAG_STEP = evaluator.evaluate(s["drag_step"])
        Config.COOLDOWN_MS = evaluator.evaluate(s["cooldown_ms"])
        Config.LOCK_DURATION_MS = evaluator.evaluate(s["lock_duration_ms"])
        Config.DOWNSCALE_FACTOR = evaluator.evaluate(s["downscale_factor"])
        Config.BOUNDARY_MARGIN = evaluator.evaluate(s["boundary_margin"])
        Config.MINIGAME_TIMEOUT_MS = evaluator.evaluate(s["minigame_timeout_ms"])

        m = data["meter_settings"]
        Config.AUTO_RELEASE_ENABLED = evaluator.evaluate(m["auto_release_enabled"])
        Config.AUTO_RELEASE_TOLERANCE = evaluator.evaluate(m["auto_release_tolerance"])
        Config.AUTO_RELEASE_CONFIDENCE = evaluator.evaluate(m["auto_release_confidence"])
        Config.AUTO_RELEASE_Y_OFFSET = evaluator.evaluate(m["auto_release_y_offset"])
        Config.SEARCH_DEPTH = evaluator.evaluate(m["search_depth"])

        r = data["routine_settings"]
        Config.AUTO_ROUTINE_ENABLED = evaluator.evaluate(r["auto_routine_enabled"])
        Config.AUTO_ROUTINE_PATTERN = tuple(
            evaluator.evaluate(x) for x in r["pattern"]
        )
        Config.AUTO_ROUTINE_WALK_TIME_MS = evaluator.evaluate(r["walk_time_ms"])
        Config.AUTO_ROUTINE_LMB_TIMEOUT_MS = evaluator.evaluate(r["lmb_timeout_ms"])

        h =data["hotkey_settings"]
        Config.TOGGLE_MOD = evaluator.evaluate(h["toggle"]["mod"])
        Config.TOGGLE_KEY = evaluator.evaluate(h["toggle"]["key"])
        Config.EXIT_MOD = evaluator.evaluate(h["exit"]["mod"])
        Config.EXIT_KEY = evaluator.evaluate(h["exit"]["key"])
        Config.MENU_MOD = evaluator.evaluate(h["menu"]["mod"])
        Config.MENU_KEY = evaluator.evaluate(h["menu"]["key"])
        Config.CANCEL_SHUTDOWN_MOD = evaluator.evaluate(h["cancel_shutdown"]["mod"])
        Config.CANCEL_SHUTDOWN_KEY = evaluator.evaluate(h["cancel_shutdown"]["key"])

        b = data["behavior_settings"]
        Config.DISCORD_WEBHOOK_ENABLED = evaluator.evaluate(b["discord_webhook_enabled"])
        Config.DISCORD_WEBHOOK_URL = b["discord_webhook_url"]
        Config.DISCORD_WEBHOOK_INTERVAL = evaluator.evaluate(b["discord_webhook_interval"])
        Config.DISCORD_WEBHOOK_RARITY_TOLERANCE = evaluator.evaluate(b["discord_webhook_rarity_tolerance"])
        Config.DISCORD_WEBHOOK_RARITY_ALERTS = {
            k.lower(): bool(v)
            for k, v in b.get("discord_webhook_rarity_alerts", {}).items()
        }
        Config.EXIT_ON_ROBLOX_DISCONNECT = evaluator.evaluate(b["exit_on_roblox_disconnect"])
        Config.SHUTDOWN_ON_ROBLOX_DISCONNECT = evaluator.evaluate(b["shutdown_on_roblox_disconnect"])
        Config.EXIT_ON_ROBLOX_KILL = evaluator.evaluate(b["exit_on_roblox_kill"])
        Config.SHUTDOWN_ON_ROBLOX_KILL = evaluator.evaluate(b["shutdown_on_roblox_kill"])

        if Config.AUTO_ROUTINE_ENABLED:
            Config.AUTO_RELEASE_ENABLED = True

    @staticmethod
    def _build_current_config():
        return {
            "description": [
                "---------------------- Bees Tool Configuration ----------------------",
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
                    "author": "",
                    "net": "",
                    "flower": ""
                },
                "app_info": {
                    "version": "1.0.0",
                    "schema": 1,
                    "created": datetime.now(timezone.utc).isoformat(),
                }
            },
            "slider_settings": {
                "confidence_threshold": Config.CONFIDENCE_THRESHOLD,
                "rotation_step":        Config.ROTATION_STEP,
                "drag_step":            Config.DRAG_STEP,
                "cooldown_ms":          Config.COOLDOWN_MS,
                "lock_duration_ms":     Config.LOCK_DURATION_MS,
                "downscale_factor":     Config.DOWNSCALE_FACTOR,
                "boundary_margin":      Config.BOUNDARY_MARGIN,
                "minigame_timeout_ms":  Config.MINIGAME_TIMEOUT_MS
            },
            "meter_settings": {
                "auto_release_enabled":    Config.AUTO_RELEASE_ENABLED,
                "auto_release_tolerance":  Config.AUTO_RELEASE_TOLERANCE,
                "auto_release_confidence": Config.AUTO_RELEASE_CONFIDENCE,
                "auto_release_y_offset":   Config.AUTO_RELEASE_Y_OFFSET,
                "search_depth":            Config.SEARCH_DEPTH
            },
            "routine_settings": {
                "auto_routine_enabled": Config.AUTO_ROUTINE_ENABLED,
                "pattern":              list(Config.AUTO_ROUTINE_PATTERN),
                "walk_time_ms":         Config.AUTO_ROUTINE_WALK_TIME_MS,
                "lmb_timeout_ms":       Config.AUTO_ROUTINE_LMB_TIMEOUT_MS
            },
            "hotkey_settings": {
                "toggle":          { "mod": Config.TOGGLE_MOD, "key": Config.TOGGLE_KEY },
                "exit":            { "mod": Config.EXIT_MOD, "key": Config.EXIT_KEY },
                "menu":            { "mod": Config.MENU_MOD, "key": Config.MENU_KEY },
                "cancel_shutdown": { "mod": Config.CANCEL_SHUTDOWN_MOD, "key": Config.CANCEL_SHUTDOWN_KEY }
            },
            "behavior_settings": {
                "discord_webhook_enabled":          Config.DISCORD_WEBHOOK_ENABLED,
                "discord_webhook_url":              Config.DISCORD_WEBHOOK_URL,
                "discord_webhook_interval":         Config.DISCORD_WEBHOOK_INTERVAL,
                "discord_webhook_rarity_tolerance": Config.DISCORD_WEBHOOK_RARITY_TOLERANCE,
                "discord_webhook_rarity_alerts":    Config.DISCORD_WEBHOOK_RARITY_ALERTS,
                "exit_on_roblox_disconnect":        Config.EXIT_ON_ROBLOX_DISCONNECT,
                "shutdown_on_roblox_disconnect":    Config.SHUTDOWN_ON_ROBLOX_DISCONNECT,
                "exit_on_roblox_kill":              Config.EXIT_ON_ROBLOX_KILL,
                "shutdown_on_roblox_kill":          Config.SHUTDOWN_ON_ROBLOX_KILL
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
            default_name = f"Bees_Tool_Config_{timestamp}.json"

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