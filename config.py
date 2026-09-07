import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class GameConfig:
    render_fps: int = 144
    resolution: tuple = (1920, 1080)
    asset_path: str = "./assets"
    debug_mode: bool = False

class SettingsRegistry:
    def __init__(self, overrides: Dict[str, Any] = None):
        self._storage = {
            "graphics": GameConfig(),
            "physics": {"gravity": -9.81, "friction": 0.5},
            "network": {"timeout": 30, "retries": 3}
        }
        if overrides:
            self._storage.update(overrides)

    def get(self, key: str, default: Any = None) -> Any:
        return self._storage.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(f"Setting '{name}' missing from game registry")

def load_environment_overrides() -> Dict[str, Any]:
    return {
        "debug_mode": os.getenv("GAME_DEBUG", "False").lower() == "true"
    }

active_config = SettingsRegistry(overrides=load_environment_overrides())