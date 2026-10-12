import time
import functools
import random

def retry_network_ops(retries=3, base_delay=1.0, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    delay = base_delay * (2 ** (attempt - 1))
                    if jitter:
                        delay += random.uniform(0, 0.1 * delay)
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_network_ops(retries=5)
def sync_game_state(payload):
    # Simulate network instability for gaming context
    if random.random() < 0.7:
        raise ConnectionError("Server lag spike detected")
    return {"status": "synced", "data": payload}