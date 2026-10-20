import time
import functools
import random

def retry_network_ops(retries=3, delay=1.0, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    if attempt == retries - 1:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_network_ops(retries=3, delay=0.5)
def fetch_game_data(endpoint):
    # Simulate network instability for gaming packets
    if random.random() < 0.7:
        raise ConnectionError('Packet drop detected')
    return {'status': 'connected', 'data': 'sync_complete'}