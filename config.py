import json
from pathlib import Path
from typing import Any, Dict

class GameConfig:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = Path(file_path)
        self.data = defaults.copy()
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if self.path.exists():
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    self.data.update(disk_data)
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def toggle(self, key: str) -> bool:
        if key in self.data and isinstance(self.data[key], bool):
            self.data[key] = not self.data[key]
            return self.data[key]
        return False

def get_loader(name: str, defaults: Dict[str, Any]) -> GameConfig:
    return GameConfig(f"{name}.json", defaults)