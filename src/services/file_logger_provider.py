import logging

from src.core.interfaces import ILoggerProvider

class FileLoggerProvider(ILoggerProvider):
    def __init__(self, formatter: logging.Formatter, file_path: str, mode: str = "a"):
        self.handler = logging.FileHandler(file_path, mode=mode, encoding="utf-8")
        self.handler.setFormatter(formatter)
        self.level = logging.DEBUG

    def configure_logger(self, logger: logging.Logger) -> None:
        logger.addHandler(self.handler)
        logger.setLevel(self.level)

    def dispose(self) -> None:
        self.handler.close()