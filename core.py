import time
import random
import functools
from typing import Callable, Any

def retry_gaming_request(attempts: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    wait = base_delay * (2 ** i) + (random.random() * 0.1)
                    time.sleep(wait)
            raise last_ex
        return wrapper
    return decorator

@retry_gaming_request(attempts=4)
def fetch_server_state(endpoint: str):
    if random.random() < 0.7:
        raise ConnectionError("Server lag spikes detected")
    return {"status": "online", "players": 42}