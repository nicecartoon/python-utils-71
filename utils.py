import time
import functools
import random

def retry_network_ops(retries=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

class GameNetworkClient:
    @retry_network_ops(retries=5, delay=1.0)
    def fetch_leaderboard(self, region):
        # Simulate unstable gaming infrastructure connectivity
        if random.random() < 0.7:
            raise ConnectionError("Server node unreachable")
        return {"region": region, "top_score": 9999}
