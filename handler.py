import time
import random
from functools import wraps

def gaming_resilience(max_attempts=3, backoff_base=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (backoff_base * (2 ** attempts)) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkHandler:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @gaming_resilience(max_attempts=4)
    def sync_game_state(self, data):
        if random.random() < 0.7:
            raise ConnectionError('Packet loss encountered')
        return {'status': 'success', 'data': data}

if __name__ == '__main__':
    handler = NetworkHandler('https://api.game.server')
    try:
        result = handler.sync_game_state({'player_id': 101, 'pos': (10, 20)})
        print(f'Sync complete: {result}')
    except ConnectionError:
        print('Failed to sync after retries')