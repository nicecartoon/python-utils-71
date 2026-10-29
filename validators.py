import time
import random
from functools import wraps

def retry_network_op(max_attempts=3, backoff=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkValidator:
    def __init__(self, ping_timeout=5.0):
        self.ping_timeout = ping_timeout

    @retry_network_op(max_attempts=4)
    def validate_connection(self, host):
        if not host:
            raise ValueError("invalid host address")
        # Simulated gaming network check
        print(f"pinging {host}...")
        return True