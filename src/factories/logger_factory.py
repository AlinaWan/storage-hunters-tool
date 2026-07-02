import logging

from core.interfaces import ILogger, ILoggerFactory, ILoggerProvider

class LoggerFactory(ILoggerFactory):
    def __init__(self):
        self._providers: list[ILoggerProvider] = []

    def add_provider(self, provider: ILoggerProvider) -> None:
        self._providers.append(provider)

    def create_logger(self, category_name: str) -> ILogger:
        logger = logging.getLogger(category_name)

        # clear existing handlers if they exist (prevents double/triple logging)
        if logger.handlers:
            logger.handlers.clear()
        
        # prevent logs from going to the root logger (where other libs live)
        logger.propagate = False
        
        # ensure every provider gets a chance to configure this
        for provider in self._providers:
            provider.configure_logger(logger)
            
        return logger

    def dispose(self) -> None:
        for provider in self._providers:
            provider.dispose()

        self._providers.clear()