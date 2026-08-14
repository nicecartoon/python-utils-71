import time
import random
import requests

class NetworkError(Exception):
    pass

def retry(func, retries=3, delay=2, backoff=2):
    for i in range(retries):
        try:
            return func()
        except NetworkError as e:
            print(f'Attempt {i + 1} failed: {e}')
            time.sleep(delay)
            delay *= backoff
    raise NetworkError('All retry attempts failed')

def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise NetworkError(f'Error fetching data: {response.status_code}')
    return response.json()

if __name__ == '__main__':
    url = 'https://api.example.com/data'
    try:
        data = retry(lambda: fetch_data(url))
        print('Fetched data:', data)
    except NetworkError as e:
        print(f'Final error: {e}')