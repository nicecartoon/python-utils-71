from typing import Dict, Any

class GameConfig:
    """A class to manage game configuration settings."""
    def __init__(self, settings: Dict[str, Any]) -> None:
        """Initialize with a settings dictionary."""
        self.settings = settings

    def get_setting(self, key: str) -> Any:
        """Retrieve a specific setting value by key."""
        return self.settings.get(key, None)

    def set_setting(self, key: str, value: Any) -> None:
        """Set a specific setting value by key."""
        self.settings[key] = value

    def __repr__(self) -> str:
        """Return a string representation of the settings."""
        return f'GameConfig({self.settings})'

# Example usage
if __name__ == '__main__':
    config = GameConfig(settings={'resolution': '1920x1080', 'volume': 75})
    print(config)
    config.set_setting('volume', 85)
    print(config.get_setting('volume'))
    