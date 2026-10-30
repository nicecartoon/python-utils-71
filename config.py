import json
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_GAMING_CONFIG: Dict[str, Any] = {
    "display": {"resolution": "1920x1080", "fullscreen": True, "fps_limit": 144, "vsync": False},
    "audio": {"master": 0.8, "sfx": 1.0, "music": 0.7, "spatial_sound": True},
    "gameplay": {"difficulty": "normal", "fov": 90, "invert_y": False, "auto_save_interval": 300},
    "keybinds": {"move_forward": "W", "move_back": "S", "use": "E", "jump": "SPACE"},
}

class ConfigSection:
    """Provides attribute-style dot access to nested gaming configuration dictionaries."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            val = self._data[name]
            return ConfigSection(val) if isinstance(val, dict) else val
        raise AttributeError(f"Configuration parameter '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._data[item]

class GamingConfigLoader:
    """Loads game configuration files with fallback engine default layers."""
    def __init__(self, config_path: Union[str, Path] = "game_settings.json"):
        self.config_path = Path(config_path)
        self._data = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        override = {}
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    override = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return self._deep_merge(DEFAULT_GAMING_CONFIG, override)

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        merged = base.copy()
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split(".")
        val = self._data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            val = self._data[name]
            return ConfigSection(val) if isinstance(val, dict) else val
        raise AttributeError(f"No top-level config category named '{name}'")
