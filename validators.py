import re
from typing import Any, Callable

class GameValidator:
    """Dynamic validator registry for game state sanitization."""
    _registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls._registry[name] = func
            return func
        return decorator

    @classmethod
    def validate(cls, name: str, value: Any) -> bool:
        return cls._registry.get(name, lambda v: True)(value)

@GameValidator.register("level_id")
def validate_level(val: Any) -> bool:
    return isinstance(val, int) and 0 <= val <= 999

@GameValidator.register("player_name")
def validate_name(val: Any) -> bool:
    return isinstance(val, str) and bool(re.match(r'^[a-zA-Z0-9_]{3,16}$', val))

@GameValidator.register("coord")
def validate_coord(val: Any) -> bool:
    return isinstance(val, (int, float)) and -10000 <= val <= 10000

def sanitize_input(key: str, data: Any) -> Any:
    """Strict boundary check for game data packets."""
    if GameValidator.validate(key, data):
        return data
    raise ValueError(f"Invalid {key} detected: {data}")