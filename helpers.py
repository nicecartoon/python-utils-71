import time
import random
import functools
from typing import Callable, Any, Type, Tuple


class GameOverException(Exception):
    """Raised when all retry attempts ('lives') are exhausted."""
    pass


def respawn_on_disconnect(
    max_lives: int = 3,
    base_cooldown: float = 0.5,
    backoff_multiplier: float = 2.0,
    retry_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator treating network retries as player respawns.
    Calculates backoff with a pseudo-random D20-based latency jitter.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            lives_remaining = max_lives
            cooldown = base_cooldown

            while lives_remaining > 0:
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as err:
                    lives_remaining -= 1
                    if lives_remaining == 0:
                        raise GameOverException(
                            f"Match connection lost after {max_lives} attempts. Failure: {err}"
                        ) from err

                    # D20 roll adds 5% to 100% variance bonus delay
                    d20_roll = random.randint(1, 20)
                    jitter = (d20_roll / 20.0) * 0.3
                    time.sleep(cooldown + jitter)
                    cooldown *= backoff_multiplier

        return wrapper
    return decorator


@respawn_on_disconnect(max_lives=4, base_cooldown=0.1, retry_exceptions=(ConnectionError, TimeoutError))
def sync_player_state(player_id: str, payload: dict) -> dict:
    """Sends player data across network with simulated drop rate."""
    if random.random() < 0.5:
        raise ConnectionError(f"Packet dropped while syncing state for {player_id}")
    return {"status": "synced", "player_id": player_id, "ack": True}
