import time
import random
import functools

def retry_operation(max_attempts=3, base_delay=1.0, jitter=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + (random.random() * jitter)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=5)
def fetch_game_data(url):
    # Simulate volatile network connection
    if random.random() < 0.7:
        raise ConnectionError("Server lag spike detected")
    return {"status": "ready", "payload": "data_packet_71"}

if __name__ == '__main__':
    data = fetch_game_data("https://api.game-node-71.io")
    print(f"Successfully retrieved: {data}")