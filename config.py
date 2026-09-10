import os
from typing import Dict, Any

class GameConfig:
    """Dynamic registry for game parameters with environmental override support."""
    _registry: Dict[str, Any] = {
        "frame_rate": 60,
        "resolution": (1920, 1080),
        "enable_physics_debug": False,
        "cache_size_mb": 512
    }

    def __init__(self, prefix: str = "GAME_"):
        self.prefix = prefix
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        for key in self._registry:
            env_key = f"{self.prefix}{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                self._registry[key] = self._parse_val(raw_val)

    def _parse_val(self, val: str) -> Any:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        try:
            return int(val)
        except ValueError:
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._registry.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._registry[key]

    def __repr__(self) -> str:
        return f"GameConfig({self._registry})"

instance = GameConfig()