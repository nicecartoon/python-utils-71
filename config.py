from typing import Dict, Any

class Config:
    """
    A class to manage game configuration settings.
    """
    def __init__(self, settings: Dict[str, Any]) -> None:
        """
        Initializes the configuration with the given settings.
        
        :param settings: A dictionary with configuration settings.
        """
        self.settings = settings

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a setting by key, returning default if key not found.
        
        :param key: The key of the setting to retrieve.
        :param default: The value to return if key is not found.
        :return: The setting value or the default.
        """
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration setting by key.
        
        :param key: The key of the setting to set.
        :param value: The value to assign to the setting.
        """
        self.settings[key] = value

    def all_settings(self) -> Dict[str, Any]:
        """
        Return all settings as a dictionary.
        
        :return: A dictionary of all settings.
        """
        return self.settings.copy()