import logging

from core.interfaces import ILoggerFactory

class LoggerMixin:
    _factory: ILoggerFactory = None 

    @classmethod
    def set_factory(cls, factory: ILoggerFactory):
        cls._factory = factory

    @property
    def logger(self):
        if self._factory is None:
            raise RuntimeError("LoggerFactory not initialized.")
            
        if not hasattr(self, '_logger'):
            # only use the class name as the logger category
            name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            self._logger = self._factory.create_logger(name)
        return self._logger

    def log_info(self, msg, *args, **kwargs):
        # stacklevel=2 allows logging to identify the method calling this helper
        self.logger.log(logging.INFO, msg, *args, stacklevel=2, **kwargs)