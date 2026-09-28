import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._data.update(json.load(f))

    def save(self, path: str) -> None:
        with open(path, 'w') as f:
            json.dump(self._data, f, indent=4)

def get_game_config(file_path: str = "settings.json") -> ConfigLoader:
    defaults = {
        "resolution": [1920, 1080],
        "vsync": True,
        "fov": 90,
        "volume": 0.8
    }
    cfg = ConfigLoader(defaults)
    cfg.load(file_path)
    return cfg

if __name__ == "__main__":
    # usage in game engine
    settings = get_game_config()
    print(f"Active resolution: {settings.resolution}")