from src.application import Application
from src.core.constants import Constants
from src.core.interfaces import IApplication, IApplicationFactory
from src.factories.logger_factory import LoggerFactory
from src.services.console_logger_provider import ConsoleLoggerProvider
from src.services.discord_webhook_logger_provider import DiscordWebhookLoggerProvider
from src.services.file_logger_provider import FileLoggerProvider
from src.utils.logger_mixin import LoggerMixin
from src.utils.logging_formatter import LoggingFormatter

class ApplicationFactory(IApplicationFactory):
    def create(self) -> IApplication:
        # new logger factory
        factory = LoggerFactory()

        if __debug__:
            formatter = LoggingFormatter

            provider = ConsoleLoggerProvider
            factory.add_provider(provider(formatter))

            if Constants.WRITE_LOGS:
                import os
                from datetime import datetime, timezone
                os.makedirs(Constants.LOG_DIR, exist_ok=True)
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                file_path = os.path.join(Constants.LOG_DIR, f"log-Storage_Hunters_Tool-{timestamp}.log")
                provider = FileLoggerProvider
                factory.add_provider(provider(file_path=file_path, formatter=formatter))

            if Constants.WRITE_DISCORD_WEBHOOK_LOGS:
                provider = DiscordWebhookLoggerProvider
                factory.add_provider(provider(webhook_url=Constants.DISCORD_WEBHOOK_LOGGER_URL, formatter=formatter))

        LoggerMixin.set_factory(factory)

        init_logger = factory.create_logger("Bootstrap")
        init_logger.info("Logger initialized and working.")

        return Application(factory=factory)