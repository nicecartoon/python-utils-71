import time
import random
from functools import wraps
from typing import Callable, Any, TypeVar

T = TypeVar('T')

class GameServerUnreachable(Exception):
    """Exception raised when game server connection drops permanently."""
    pass

def retry_network_op(
    max_respawns: int = 3,
    cooldown_sec: float = 0.2,
    backoff_multiplier: float = 2.0,
    ping_jitter: bool = True
) -> Callable:
    """Retries game network operations with exponential cooldown and ping jitter."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = cooldown_sec
            for attempt in range(1, max_respawns + 2):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt > max_respawns:
                        raise GameServerUnreachable(
                            f"Operation '{func.__name__}' failed after {max_respawns} retries"
                        ) from exc
                    
                    jitter = random.uniform(0.85, 1.15) if ping_jitter else 1.0
                    sleep_duration = delay * jitter
                    time.sleep(sleep_duration)
                    delay *= backoff_multiplier
            raise GameServerUnreachable("Unexpected retry exhaustion")
        return wrapper
    return decorator