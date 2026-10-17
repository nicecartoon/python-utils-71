import json
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_GAMING_CONFIG: Dict[str, Any] = {
    "graphics": {"fps_limit": 144, "fov": 90, "vsync": False, "quality": "high"},
    "audio": {"master_volume": 0.8, "sfx_volume": 1.0, "music_volume": 0.5},
    "controls": {"invert_y": False, "sensitivity": 1.2, "keybinds": {"jump": "SPACE", "crouch": "C"}},
    "gameplay": {"difficulty": "normal", "subtitles": True}
}

class GamingConfig(dict):
    """Attribute-accessible config object with recursive default merging."""

    def __init__(self, data: Dict[str, Any] = None, defaults: Dict[str, Any] = None):
        merged = dict(defaults or DEFAULT_GAMING_CONFIG)
        if data:
            self._deep_merge(merged, data)
        super().__init__(merged)
        
        for key, value in list(self.items()):
            if isinstance(value, dict):
                self[key] = GamingConfig(value, defaults={})

    def _deep_merge(self, target: dict, source: dict):
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"Configuration setting '{item}' does not exist")

    def __setattr__(self, key: str, value: Any):
        self[key] = value

    @classmethod
    def load_from_file(cls, path: Union[str, Path], defaults: Dict[str, Any] = None) -> "GamingConfig":
        config_path = Path(path)
        if not config_path.exists():
            return cls(defaults=defaults)
        
        with open(config_path, "r", encoding="utf-8") as file_handle:
            content = json.load(file_handle)
        return cls(data=content, defaults=defaults)

    def save_to_file(self, path: Union[str, Path]) -> None:
        config_path = Path(path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as file_handle:
            json.dump(self, file_handle, indent=4)
