import json
import os
from typing import Any, Dict

def load_game_config(path: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """ recursively merge file content with defaults """
    if not os.path.exists(path):
        return defaults
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    def deep_merge(target: Dict, source: Dict) -> Dict:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                deep_merge(target[key], value)
            else:
                target[key] = value
        return target

    return deep_merge(defaults.copy(), data)

class ConfigProxy:
    """ allows dot notation for dictionary access """
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __getattr__(self, item: str) -> Any:
        return self.__dict__.get(item, None)

if __name__ == '__main__':
    base = {'resolution': [1920, 1080], 'volume': 75, 'graphics': {'shadows': True}}
    cfg = load_game_config('settings.json', base)
    settings = ConfigProxy(cfg)
    print(f'current volume: {settings.volume}')