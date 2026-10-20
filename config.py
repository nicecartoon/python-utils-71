import os
import json
import logging

class ConfigLoader:
    def __init__(self, path='settings.json'):
        self.path = path
        self.data = {}

    def load_gaming_profile(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError('Config missing, defaulting to console mode')
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f'Config fault: {e}. Using fallback defaults.')
            self.data = {'fps_cap': 60, 'vsync': True, 'mode': 'safe'}
        return self.data

    def get_setting(self, key, default):
        try:
            return self.data.get(key, default)
        except AttributeError:
            return default

    def validate_performance(self):
        if self.data.get('fps_cap', 0) < 30:
            self.data['fps_cap'] = 30
            print('Warning: Performance floor triggered')
        return True

# Global config singleton for gaming session
config_manager = ConfigLoader()
config_manager.load_gaming_profile()