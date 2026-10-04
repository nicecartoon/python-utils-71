import time
import random
from typing import Callable, Any, TypeVar
from functools import wraps

F = TypeVar("F", bound=Callable[..., Any])

class RespawnExhaustedError(Exception):
    """Raised when network retries run out of player lives."""
    pass

def network_respawn(
    max_lives: int = 3,
    base_cooldown: float = 0.2,
    max_cooldown: float = 4.0,
    critical_hit_jitter: bool = True,
    target_exceptions: tuple[type[BaseException], ...] = (Exception,)
) -> Callable[[F], F]:
    """Decorator providing exponential backoff with gaming-inspired retry logic."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            lives = max_lives
            current_delay = base_cooldown

            while lives > 0:
                try:
                    return func(*args, **kwargs)
                except target_exceptions as err:
                    lives -= 1
                    if lives == 0:
                        raise RespawnExhaustedError(
                            f"Call '{func.__name__}' failed after {max_lives} retries. "
                            f"Final error: {err}"
                        ) from err

                    jitter = random.uniform(0.05, 0.25) if critical_hit_jitter else 0.0
                    sleep_time = min(current_delay + jitter, max_cooldown)
                    time.sleep(sleep_time)
                    current_delay *= 2.0

        return wrapper  # type: ignore
    return decorator
