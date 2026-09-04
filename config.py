import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], filepath: str = 'settings.json'):
        self.filepath = filepath
        self.data = defaults.copy()
        self._load_file()

    def _load_file(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    user_data = json.load(f)
                    self.data.update(user_data)
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'Setting {name} not found in configuration')

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def persist(self) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def update_settings(self, new_data: Dict[str, Any]) -> None:
        self.data.update(new_data)
        self.persist()