DEFAULTS = {
    'difficulty': 'normal',
    'volume': 50,
    'fullscreen': True,
    'resolution': (1920, 1080)
}

class ConfigLoader:
    def __init__(self, user_config=None):
        self.config = DEFAULTS.copy()  # Start with defaults
        if user_config:
            self.load_user_config(user_config)

    def load_user_config(self, user_config):
        for key, value in user_config.items():
            if key in self.config:
                self.config[key] = value

    def get(self, key):
        return self.config.get(key, None)

if __name__ == '__main__':
    user_preferences = {
        'volume': 75,
        'resolution': (1280, 720)
    }
    config = ConfigLoader(user_preferences)
    print(config.config)  # Displays merged configuration
