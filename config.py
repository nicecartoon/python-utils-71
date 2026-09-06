import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if not os.path.exists(path):
            return
        with open(path, 'r') as f:
            user_config = json.load(f)
            self._recursive_update(self._data, user_config)

    def _recursive_update(self, base: Dict, patch: Dict) -> None:
        for key, value in patch.items():
            if isinstance(value, dict) and key in base:
                self._recursive_update(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config key {name} missing')

    def __repr__(self) -> str:
        return f'ConfigManager(keys={list(self._data.keys())})'