from typing import Union, Callable, Any

def validate_game_state(state: dict[str, Any]) -> bool:
    """Checks if player stats are within the game balance limits."""
    limits = {'health': (0, 100), 'mana': (0, 500), 'xp': (0, float('inf'))}
    return all(limits[k][0] <= state[k] <= limits[k][1] for k in limits if k in state)

def sanitize_input(data: Union[str, int]) -> str:
    """Cleans player input to prevent injection in game chat."""
    return str(data).replace('<', '').replace('>', '').strip()

def chain_validator(func: Callable[[Any], bool], fallback: Any) -> Callable[[Any], Any]:
    """Higher order function wrapper for risky data processing."""
    def wrapper(value: Any) -> Any:
        try:
            return value if func(value) else fallback
        except Exception:
            return fallback
    return wrapper

check_level_cap = chain_validator(lambda x: isinstance(x, int) and x < 99, 1)