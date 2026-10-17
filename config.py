import json
import os
from typing import Any, Dict

class GameConfig:
    def __init__(self, path: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.data = defaults or {}
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    self.data.update(disk_data)
            except (json.JSONDecodeError, IOError):
                pass

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def persist(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

def get_config(name: str = 'core') -> GameConfig:
    defaults = {'fps': 60, 'resolution': (1920, 1080), 'debug': False}
    return GameConfig(f'{name}_cfg.json', defaults)