import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type


class RageQuitException(Exception):
    """Raised when maximum network retry attempts (wipes) are exhausted."""
    pass


def retry_on_wipe(
    max_lives: int = 3,
    base_cooldown: float = 0.5,
    rage_quit_exceptions: Tuple[Type[Exception], ...] = (),
    critical_clutch_chance: float = 0.15
) -> Callable:
    """
    Retries a gaming network operation using a respawn-timer algorithm.
    Features exponential backoff with jitter and an instant 'clutch' recovery chance.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            lives_left = max_lives
            wipe_count = 0
            
            while lives_left > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if isinstance(error, rage_quit_exceptions):
                        raise error
                    
                    lives_left -= 1
                    wipe_count += 1
                    
                    if lives_left <= 0:
                        raise RageQuitException(
                            f"Party wiped in '{func.__name__}' after {max_lives} retries. Cause: {error}"
                        ) from error
                    
                    # Roll for instant clutch respawn (bypasses long cooldown)
                    is_clutch = random.random() < critical_clutch_chance
                    if is_clutch:
                        cooldown = 0.05
                    else:
                        jitter = random.uniform(0.85, 1.25)
                        cooldown = (base_cooldown * (2 ** (wipe_count - 1))) * jitter
                    
                    time.sleep(cooldown)
        return wrapper
    return decorator