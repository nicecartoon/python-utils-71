import time
import functools
import random

class NetworkGlitch(Exception):
    pass

def retry_gaming_request(retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, NetworkGlitch) as e:
                    last_ex = e
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** attempt)) + jitter
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class PacketProcessor:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @retry_gaming_request(retries=5, base_delay=0.5)
    def sync_game_state(self, payload):
        if random.random() < 0.3:
            raise NetworkGlitch("Packet drop detected by server")
        return {"status": "synced", "data": payload}

def process_player_input(processor, data):
    try:
        return processor.sync_game_state(data)
    except Exception as e:
        return {"error": str(e), "status": "failed"}