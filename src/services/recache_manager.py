from typing import final as sealed, Callable as Action

@sealed
class RecacheManager:
    def __init__(self):
        self._callbacks: list[Action[[], None]] = []
        self._pending = False

    def register(self, callback: Action[[], None]):
        self._callbacks.append(callback)

    def trigger(self):
        self._pending = True

    def flush(self):
        if not self._pending:
            return

        self._pending = False

        for cb in self._callbacks:
            try:
                cb()
            except Exception as e:
                print(f"[RecacheManager::Trigger] Callback error: {e}")