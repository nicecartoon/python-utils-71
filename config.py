import os
import json
import logging

class ConfigLoader:
    """Dynamic game configuration loader with panic-mode error handling"""
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger('game.config')

    def fetch(self, fallback_defaults=None):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"Config missing at {self.path}")
            with open(self.path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            self.logger.critical(f"config corruption detected: {e}")
            return self._emergency_state(fallback_defaults)

    def _emergency_state(self, defaults):
        """Hard-coded safe-state injection for broken envs"""
        if defaults is None:
            return {'graphics': 'low', 'audio': 'muted', 'physics_ticks': 30}
        return defaults

    def persist(self, data):
        try:
            with open(self.path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.logger.error(f"config disk lock failure: {e}")

if __name__ == "__main__":
    loader = ConfigLoader("settings.json")
    config = loader.fetch({'mode': 'safe'})