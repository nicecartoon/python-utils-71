import json
from typing import Any, Dict

class GameConfigStore:
    def __init__(self, filepath: str = 'settings.json'):
        self.path = filepath
        self.data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {'master_volume': 0.8, 'resolution': (1920, 1080), 'cheats_enabled': False}

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def update_setting(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

    def _save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.update_setting(key, value)

def get_session_manager() -> GameConfigStore:
    return GameConfigStore()