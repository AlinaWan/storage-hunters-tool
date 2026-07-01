import logging

from core.interfaces import ILoggerProvider

class ConsoleLoggerProvider(ILoggerProvider):
    def __init__(self, formatter: logging.Formatter):
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(formatter)
        self.level = logging.DEBUG

    def configure_logger(self, logger: logging.Logger) -> None:
        logger.addHandler(self.handler)
        logger.setLevel(self.level)

    def dispose(self) -> None:
        self.handler.close()