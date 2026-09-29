import time
import functools
import random

def retry_operation(max_retries=3, base_delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_operation(max_retries=5)
def fetch_game_server_data(endpoint):
    # Simulate volatile gaming network conditions
    if random.random() < 0.7:
        raise ConnectionError("Packet loss detected")
    return {"status": "online", "players": 42}