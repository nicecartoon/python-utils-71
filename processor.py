import time
import random
import requests

class NetworkError(Exception):
    pass

class Retry:
    def __init__(self, attempts=3, delay=2, backoff=2):
        self.attempts = attempts
        self.delay = delay
        self.backoff = backoff

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for attempt in range(self.attempts):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, NetworkError) as e:
                    if attempt < self.attempts - 1:
                        time.sleep(self.delay)
                        self.delay *= self.backoff
                    else:
                        raise
        return wrapper

@Retry(attempts=5, delay=1)
def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise NetworkError(f'Failed to fetch data, status code: {response.status_code}')
    return response.json()

if __name__ == '__main__':
    try:
        data = fetch_data('https://api.example.com/data')
        print(data)
    except NetworkError as e:
        print(f'Error: {e}')
