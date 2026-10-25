import json
import os
from typing import Any, Dict

DEFAULT_GAMING_CONFIG: Dict[str, Any] = {
    "graphics": {
        "resolution": "1920x1080",
        "fps_limit": 144,
        "vsync": True,
        "fov": 90.0,
    },
    "audio": {
        "master_volume": 0.8,
        "sfx_volume": 1.0,
        "music_volume": 0.5,
        "mute_in_background": True,
    },
    "controls": {
        "mouse_sensitivity": 1.2,
        "invert_y": False,
        "keybinds": {"jump": "space", "crouch": "c", "interact": "e"},
    },
    "debug": {"show_fps": False, "god_mode": False},
}


class ConfigNode:
    """Wrapper enabling dot-notation and dynamic default fallback for game settings."""

    def __init__(self, data: Dict[str, Any], defaults: Dict[str, Any] = None):
        self._data = data
        self._defaults = defaults or {}

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            val = self._data[name]
            def_val = self._defaults.get(name)
        elif name in self._defaults:
            val = self._defaults[name]
            def_val = val
        else:
            raise AttributeError(f"Configuration key '{name}' not found.")

        if isinstance(val, dict):
            return ConfigNode(val, def_val if isinstance(def_val, dict) else {})
        return val

    def get(self, key: str, fallback: Any = None) -> Any:
        try:
            return getattr(self, key)
        except AttributeError:
            return fallback


class GameConfigLoader:
    """Loads game configuration files with fallback to preset gaming defaults."""

    def __init__(self, default_config: Dict[str, Any] = None):
        self.defaults = default_config or DEFAULT_GAMING_CONFIG

    def load_from_file(self, filepath: str) -> ConfigNode:
        loaded = {}
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        return ConfigNode(loaded, self.defaults)
