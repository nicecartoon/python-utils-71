import random
import time
from typing import Callable, Any, Tuple, Type

class NetworkGlitch(Exception):
    """Base exception for transient gaming network anomalies."""
    pass

class LagSpikeError(NetworkGlitch):
    """Temporary latency spike, highly recoverable."""
    pass

class PacketLossError(NetworkGlitch):
    """Dropped frames or packets, requires aggressive retry."""
    pass

class MatchmakingTimeoutError(NetworkGlitch):
    """Connection timeout to matchmaker, retry recommended."""
    pass

def self_healing(
    max_retries: int = 5,
    base_delay: float = 0.1,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (NetworkGlitch,)
):
    """
    Fibonacci-based backoff decorator specifically tuned for gaming micro-outages.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            a, b = 1, 1
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise e
                    delay = a * base_delay
                    if jitter:
                        delay += random.uniform(0.01, 0.05)
                    time.sleep(delay)
                    a, b = b, a + b
        return wrapper
    return decorator