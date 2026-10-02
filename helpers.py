import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('game_engine')

class GameStateError(Exception):
    """Custom error for corrupted game states."""
    pass

def safety_net(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            logger.error(f'Oopsie in {func.__name__}: {e}')
            return None
        except Exception as fatal:
            logger.critical(f'Game engine collapse: {fatal}')
            raise GameStateError(f'Fatal sync issue in {func.__name__}') from fatal
    return wrapper

@safety_net
def calculate_damage(base: int, multiplier: float) -> float:
    if base < 0:
        raise ValueError('Damage cannot be negative')
    return float(base * multiplier)

def sanitize_input(data: Any) -> str:
    try:
        return str(data).strip()[:128]
    except Exception:
        return 'invalid_data'