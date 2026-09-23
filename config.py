import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults for game settings."""
    def __init__(self, default_path: str = "defaults.json"):
        self.defaults = self._load_file(default_path)

    def _load_file(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def load(self, user_config_path: str) -> Dict[str, Any]:
        user_data = self._load_file(user_config_path)
        return self._merge(self.defaults, user_data)

    def _merge(self, base: Dict, patch: Dict) -> Dict:
        result = base.copy()
        for key, value in patch.items():
            if isinstance(value, dict) and key in result:
                result[key] = self._merge(result[key], value)
            else:
                result[key] = value
        return result

def get_game_config(path: str) -> Dict[str, Any]:
    loader = ConfigLoader()
    return loader.load(path)