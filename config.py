import json
import os

class ConfigLoader:
    def __init__(self, default_config, user_config_path):
        self.default_config = default_config
        self.user_config_path = user_config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.user_config_path):
            with open(self.user_config_path, 'r') as user_config_file:
                user_config = json.load(user_config_file)
            return self.merge_configs(user_config)
        return self.default_config

    def merge_configs(self, user_config):
        merged_config = self.default_config.copy()
        merged_config.update(user_config)
        return merged_config

# Example default configuration
DEFAULT_CONFIG = {
    'resolution': '1920x1080',
    'fullscreen': True,
    'volume': 75,
}

# Usage
# loader = ConfigLoader(DEFAULT_CONFIG, 'user_config.json')
# print(loader.config)
