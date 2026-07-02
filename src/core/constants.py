from pathlib import Path
from typing import Final as ReadOnly, final as sealed

from src.core.native_methods import NativeMethods
from src.services.console_logger_provider import ConsoleLoggerProvider
from src.services.discord_webhook_logger_provider import DiscordWebhookLoggerProvider
from src.services.file_logger_provider import FileLoggerProvider
from src.utils.logging_formatter import LoggingFormatter

@sealed
class Constants:

    SCRIPT_DIR: ReadOnly = Path(__file__).resolve().parent.parent # src\ dir
    WINDOWS_DIR: ReadOnly = Path(NativeMethods.get_windows_directory())

    CONSOLE_LOGGER_PROVIDER: ReadOnly = ConsoleLoggerProvider
    FILE_LOGGER_PROVIDER: ReadOnly = FileLoggerProvider
    DISCORD_WEBHOOK_LOGGER_PROVIDER: ReadOnly = DiscordWebhookLoggerProvider
    LOGGING_FORMATTER: ReadOnly = LoggingFormatter
    LOG_DIR: ReadOnly = "logs"
    WRITE_LOGS: ReadOnly = False
    WRITE_DISCORD_WEBHOOK_LOGS: ReadOnly = False
    DISCORD_WEBHOOK_LOGGER_URL: ReadOnly = ""

    TEXT_EDITOR_PATH: ReadOnly = WINDOWS_DIR / "System32" / "notepad.exe"

    SCREEN_WIDTH: ReadOnly = NativeMethods.get_screen_width()
    SCREEN_HEIGHT: ReadOnly = NativeMethods.get_screen_height()

    GUID: ReadOnly = "1ad6d4b8-78ae-4aa0-974d-a12c88a0d77e"
    GITHUB_URL: ReadOnly = "https://github.com/AlinaWan/storage-hunters-tool"
    DISCORD_APPLICATION_ID: ReadOnly = "1521762355158057031"