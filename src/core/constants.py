from pathlib import Path
from typing import Final as ReadOnly, final as sealed

from core.native_methods import NativeMethods

@sealed
class Constants:

    SCRIPT_DIR: ReadOnly = Path(__file__).resolve().parent.parent # src\ dir
    WINDOWS_DIR: ReadOnly = Path(NativeMethods.get_windows_directory())

    TEXT_EDITOR_PATH: ReadOnly = WINDOWS_DIR / "System32" / "notepad.exe"

    SCREEN_WIDTH: ReadOnly = NativeMethods.get_screen_width()
    SCREEN_HEIGHT: ReadOnly = NativeMethods.get_screen_height()

    GUID: ReadOnly = "1ad6d4b8-78ae-4aa0-974d-a12c88a0d77e"
    GITHUB_URL: ReadOnly = "https://github.com/AlinaWan/storage-hunters-tool"
    DISCORD_APPLICATION_ID: ReadOnly = "1521762355158057031"