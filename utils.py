import functools
import random
import time
from typing import Any, Callable, Dict


class ServerLagError(Exception):
    """Exception raised when game server fails to respond after retries."""

    pass


class NetworkRespawningManager:
    """Manages network call attempts with exponential stamina delay and jitter."""

    def __init__(self, max_lives: int = 4, base_delay: float = 0.15):
        self.max_lives = max_lives
        self.base_delay = base_delay
        self.stats: Dict[str, Any] = {"attempts": 0, "total_wait": 0.0}

    def invoke(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        lives = self.max_lives
        current_delay = self.base_delay

        while lives > 0:
            self.stats["attempts"] += 1
            try:
                return func(*args, **kwargs)
            except Exception as err:
                lives -= 1
                if lives <= 0:
                    raise ServerLagError(
                        f"Execution failed after {self.max_lives} respawn attempts."
                    ) from err

                jitter = random.uniform(0.05, 0.2)
                wait_time = current_delay + jitter
                self.stats["total_wait"] += wait_time
                time.sleep(wait_time)
                current_delay *= 2.0


def respawn_on_drop(
    max_lives: int = 3, base_delay: float = 0.1
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for auto-retrying failed network operations in multiplayer context."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            manager = NetworkRespawningManager(
                max_lives=max_lives, base_delay=base_delay
            )
            return manager.invoke(func, *args, **kwargs)

        return wrapper

    return decorator
