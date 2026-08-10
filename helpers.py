import time
import requests
from functools import wraps


def retry(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.Timeout) as e:
                    attempts += 1
                    print(f'Attempt {attempts} failed: {e}')
                    if attempts == max_retries:
                        print('Max retries reached. Raising exception.')
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_retries=5, delay=3)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# Example usage
if __name__ == '__main__':
    try:
        data = fetch_data('https://api.example.com/data')
        print(data)
    except Exception as e:
        print(f'Failed to fetch data: {e}')