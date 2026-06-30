from typing import Protocol

class IDisposable(Protocol):
    def dispose(self) -> None: ...