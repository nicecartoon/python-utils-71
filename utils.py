import time
import random
import requests

class RetryException(Exception):
    pass

def retry_request(url, max_retries=3, delay=1):
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Assuming we expect JSON response
        except (requests.ConnectionError, requests.Timeout) as e:
            attempts += 1
            if attempts >= max_retries:
                raise RetryException(f'Request failed after {max_retries} attempts: {e}')
            wait_time = delay * (2 ** attempts) + random.uniform(0, 1)
            time.sleep(wait_time)  # Exponential backoff with jitter
        except requests.HTTPError as e:
            raise RetryException(f'HTTP error occurred: {e}')
    return None

# Example usage
# result = retry_request('https://api.example.com/data')
# print(result)