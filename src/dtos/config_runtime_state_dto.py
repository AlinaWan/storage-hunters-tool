from typing import Any as Dynamic, final as sealed

from services.file_watcher import FileWatcher

@sealed
class ConfigRuntimeStateDto:
    def __init__(self):

        self.config_watcher: FileWatcher = FileWatcher()
        self.current_config_path: str | None = None
        self.config_data: Dynamic = None
        self.recache_manager: Dynamic = None