import functools
import random
import time
from typing import Any, Callable, Tuple, Type


class NetworkLagError(Exception):
    """Raised when a game network request encounters severe latency or packet loss."""

    pass


class ServerUnreachableError(Exception):
    """Raised when matchmaking or game state retry attempts are completely exhausted."""

    pass


def respawn_retry(
    max_lives: int = 4,
    base_cooldown: float = 0.2,
    allowed_exceptions: Tuple[Type[Exception], ...] = (
        NetworkLagError,
        ConnectionError,
        TimeoutError,
    ),
) -> Callable:
    """Retry decorator utilizing exponential backoff with gaming-inspired RNG jitter."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            stamina = 1.0
            while attempts < max_lives:
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as err:
                    attempts += 1
                    if attempts >= max_lives:
                        raise ServerUnreachableError(
                            f"Packet delivery failed after {max_lives} respawns. Reason: {err}"
                        ) from err

                    critical_roll = random.randint(1, 20)
                    backoff = base_cooldown * (1.8**attempts) * (2.0 - stamina)

                    if critical_roll == 20:
                        backoff *= 0.1
                    elif critical_roll == 1:
                        backoff *= 2.0

                    time.sleep(max(0.05, backoff))
                    stamina = max(0.1, stamina - 0.25)

        return wrapper

    return decorator


@respawn_retry(max_lives=3, base_cooldown=0.1)
def transmit_match_snapshot(endpoint: str, match_data: dict) -> dict:
    """Transmits player match snapshot over simulated volatile game server connection."""
    if random.random() < 0.5:
        raise NetworkLagError("Lag spike detected during UDP snapshot sync")
    return {
        "status": "ack",
        "endpoint": endpoint,
        "bytes_sent": len(str(match_data)),
    }
