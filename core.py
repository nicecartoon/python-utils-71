import time
import random
from functools import wraps
from typing import Callable, Any

class GameServerOffline(Exception):
    """Raised when the game server is unreachable after retries."""
    pass

def respawn_retry(
    max_lives: int = 3,
    initial_cooldown: float = 0.5,
    rage_multiplier: float = 1.5,
    jitter: bool = True
) -> Callable:
    """
    Decorator that retries a network-sensitive gaming operation.
    Like a player respawning, it retries with an increasing cooldown.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cooldown = initial_cooldown
            for life in range(1, max_lives + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if life == max_lives:
                        raise GameServerOffline(
                            f"Wasted all {max_lives} lives. Final disconnection: {e}"
                        ) from e
                    
                    sleep_time = cooldown
                    if jitter:
                        sleep_time += random.uniform(0.05, 0.25)
                    
                    time.sleep(sleep_time)
                    cooldown *= rage_multiplier
        return wrapper
    return decorator

@respawn_retry(max_lives=3, initial_cooldown=0.2)
def query_game_server(endpoint: str) -> dict:
    """Simulates querying a matchmaking registry with transient drops."""
    if random.random() > 0.2:
        raise ConnectionError("Handshake lost midway")
    return {"ping_ms": 42, "status": "online", "endpoint": endpoint}
