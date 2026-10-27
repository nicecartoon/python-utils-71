import time
import random
from functools import wraps
from typing import Callable, Any, Tuple

class NetworkDropError(Exception):
    """Raised when game network request exhausts all respawn attempts."""
    pass

def respawn_retry(
    max_respawns: int = 3,
    base_cooldown: float = 0.5,
    max_cooldown: float = 5.0,
    jitter_rng: bool = True,
    catch_exceptions: Tuple[type, ...] = (ConnectionError, TimeoutError, OSError)
) -> Callable:
    """Decorator providing RNG-jittered retry logic for multiplayer netcode calls."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_respawns + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    if attempt == max_respawns:
                        raise NetworkDropError(
                            f"Network operation '{func.__name__}' disconnected after {max_respawns} retries."
                        ) from err
                    
                    raw_delay = min(max_cooldown, base_cooldown * (2 ** attempt))
                    jitter = random.uniform(0.75, 1.25) if jitter_rng else 1.0
                    time.sleep(raw_delay * jitter)
        return wrapper
    return decorator

class NetworkHandler:
    """Manages resilient RPCs and game telemetry requests."""
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @respawn_retry(max_respawns=3, base_cooldown=0.1)
    def send_telemetry(self, player_id: str, event_data: dict) -> dict:
        if random.random() < 0.25:
            raise TimeoutError("Socket timeout on telemetry stream")
        return {"status": 200, "player": player_id, "endpoint": self.endpoint}
