import functools
import random
import time
from typing import Callable, Any

class NetworkDisconnectError(Exception):
    """Raised when the gaming network bridge collapses."""
    pass

def _fibonacci_cooldowns(base: float):
    """Generator mimicking gaming recovery intervals using Fibonacci sequence."""
    a, b = base, base * 2
    while True:
        yield a
        a, b = b, a + b

def respawn_on_disconnect(lives: int = 3, base_cooldown: float = 0.5) -> Callable:
    """
    Decorator mimicking a 'respawn' mechanism for network operations.
    Spends a 'life' and cools down before retrying the operation.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cooldown_gen = _fibonacci_cooldowns(base_cooldown)
            remaining_lives = lives
            
            while remaining_lives > 0:
                try:
                    return func(*args, **kwargs)
                except NetworkDisconnectError as exc:
                    remaining_lives -= 1
                    if remaining_lives <= 0:
                        raise RuntimeError("Game Over: Network connection lost permanently.") from exc
                    
                    sleep_time = next(cooldown_gen) + random.uniform(0.01, 0.1)
                    time.sleep(sleep_time)
            
        return wrapper
    return decorator

# Simulated network action mimicking server connection status
@respawn_on_disconnect(lives=4, base_cooldown=0.1)
def fetch_matchmaking_lobby(player_id: str) -> dict:
    """Attempts to reach the matchmaking server with built-in retry fallback."""
    if random.random() > 0.4:  
        raise NetworkDisconnectError(f"Lobby sync failed for player {player_id}")
    return {"status": "connected", "lobby_id": "nexus-7", "latency_ms": 42}
