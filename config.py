import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic gaming configuration injector with fallback magic."""
    def __init__(self, defaults: Dict[str, Any]):
        self.config = defaults

    def load_from_json(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                user_cfg = json.load(f)
                self.config.update(user_cfg)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self.config:
            return self.config[name]
        raise AttributeError(f'Config item {name} not found')

def get_game_config() -> ConfigLoader:
    defaults = {
        "resolution": "1920x1080",
        "vsync": True,
        "fov": 90,
        "sensitivity": 1.5
    }
    loader = ConfigLoader(defaults)
    loader.load_from_json("settings.json")
    return loader

cfg = get_game_config()