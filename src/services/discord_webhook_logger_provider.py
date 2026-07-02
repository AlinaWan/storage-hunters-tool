import logging

from src.core.interfaces import ILoggerProvider
from src.services.discord_webhook_logger_handler import DiscordWebhookLoggerHandler
from src.utils.discord_webhook_payload_formatter import DiscordWebhookPayloadFormatter

class DiscordWebhookLoggerProvider(ILoggerProvider):
    def __init__(self, formatter: logging.Formatter, webhook_url: str):
        self.handler = DiscordWebhookLoggerHandler(webhook_url, DiscordWebhookPayloadFormatter())
        self.handler.setFormatter(formatter)
        self.level = logging.INFO

    def configure_logger(self, logger: logging.Logger) -> None:
        logger.addHandler(self.handler)
        logger.setLevel(self.level)

    def dispose(self):
        self.handler.close()