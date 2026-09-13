import time
import random
import functools
from typing import Callable, Any, Optional

class NetworkPacketRetry:
    """Retry handler tailored for latency-sensitive gaming network requests."""

    def __init__(self, max_retries: int = 3, base_delay: float = 0.1, max_delay: float = 2.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None
            for attempt in range(1, self.max_retries + 2):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt > self.max_retries:
                        break
                    delay = min(self.max_delay, self.base_delay * (2 ** (attempt - 1)))
                    jitter = random.uniform(0, delay * 0.5)
                    time.sleep(delay + jitter)
            if last_exception:
                raise last_exception
        return wrapper

def send_game_telemetry(payload: dict) -> bool:
    """Example function using retry decorator for game network calls."""
    @NetworkPacketRetry(max_retries=4, base_delay=0.05)
    def _dispatch():
        if random.random() < 0.7:
            raise ConnectionError("Packet dropped in game session pipeline")
        return True
    return _dispatch()