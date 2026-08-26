from typing import Dict, Any, Optional

class GameConfig:
    """Runtime configuration manager for gaming utilities."""
    
    def __init__(self, default_fps: int = 60, v_sync: bool = True) -> None:
        self._settings: Dict[str, Any] = {
            "fps": default_fps,
            "vsync": v_sync,
            "audio_channels": 128,
            "cheat_codes_active": False
        }

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a configuration value by its unique key."""
        return self._settings.get(key, None)

    def set(self, key: str, value: Any) -> None:
        """Mutate or create a configuration parameter on the fly."""
        self._settings[key] = value

    def toggle_cheats(self) -> bool:
        """Secret toggle for gaming diagnostic overlays."""
        current: bool = self._settings["cheat_codes_active"]
        self._settings["cheat_codes_active"] = not current
        return self._settings["cheat_codes_active"]

active_config = GameConfig()