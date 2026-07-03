import logging

from typing import Protocol, runtime_checkable

class IApplication(Protocol):
    def run(self) -> None: ...
    def current_domain_process_exit(self) -> None: ...

class IApplicationFactory(Protocol):
    def create(self) -> IApplication: ...

class IApplicationOrchestrator(Protocol):
    factory: IApplicationFactory
    def run(self) -> None: ...

class IDisposable(Protocol):
    def dispose(self) -> None: ...

@runtime_checkable
class ILogger(Protocol):
    def log(self, level: int, msg: str, *args, **kwargs) -> None: ...

@runtime_checkable
class ILoggerProvider(IDisposable, Protocol):
    def configure_logger(self, logger: logging.Logger) -> None: ...

@runtime_checkable
class ILoggerFactory(IDisposable, Protocol):
    def add_provider(self, provider: ILoggerProvider) -> None: ...
    def create_logger(self, category_name: str) -> ILogger: ...
