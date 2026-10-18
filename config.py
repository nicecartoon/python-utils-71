import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'settings.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def persist(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def initialize_game_config() -> ConfigLoader:
    defaults = {
        "resolution": "1920x1080",
        "vsync": True,
        "fov": 90,
        "volume": 0.8
    }
    return ConfigLoader('config.json', defaults)