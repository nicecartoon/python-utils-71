import json
import os

class GameConfig:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        if not os.path.isfile(self.config_file):
            raise FileNotFoundError(f'Configuration file {self.config_file} does not exist.')
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def get_setting(self, key, default=None):
        return self.config_data.get(key, default)

    def set_setting(self, key, value):
        self.config_data[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)

config = GameConfig()  # Instance of GameConfig for easy access

