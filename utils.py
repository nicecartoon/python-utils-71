import time
import functools
import random
from typing import Callable, Any

def retry_network_op(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

@retry_network_op(max_attempts=5)
def fetch_game_server_data(endpoint: str):
    # Simulate sporadic gaming API instability
    if random.random() < 0.7:
        raise ConnectionError("Server handshake failed")
    return {"status": "ready", "endpoint": endpoint}