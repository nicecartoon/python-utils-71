import os
import json
import logging

class ConfigError(Exception):
    pass

def load_game_config(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config missing: {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise TypeError("Config structure malformed")
            
        return {k: v for k, v in data.items() if v is not None}

    except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
        logging.error(f"Configuration failure: {e}")
        return {"resolution": "1920x1080", "vsync": True, "fallback": True}

def validate_settings(settings):
    keys = ['resolution', 'vsync']
    try:
        missing = [k for k in keys if k not in settings]
        if missing:
            raise ConfigError(f"Missing critical keys: {missing}")
        
        if 'x' not in settings['resolution']:
            raise ValueError("Invalid resolution format")
            
        return True
    except (ConfigError, ValueError) as e:
        logging.warning(f"Validation bypass triggered: {e}")
        return False

settings = load_game_config('settings.json')
ready = validate_settings(settings)