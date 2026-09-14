import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    loaded = json.load(f)
                    self.data.update({k: v for k, v in loaded.items() if k in self.data})
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def get_game_config():
    defaults = {
        "resolution": "1920x1080",
        "fullscreen": True,
        "volume": 0.8,
        "fps_limit": 144
    }
    return ConfigLoader("settings.json", defaults)