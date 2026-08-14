import time
import requests

class RetryException(Exception):
    pass


def retry_request(url, retries=5, backoff=1.0):
    tries = 0
    while tries < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Assuming we want JSON data
        except requests.exceptions.RequestException as e:
            tries += 1
            if tries == retries:
                raise RetryException(f'Failed to retrieve {url} after {retries} attempts') from e
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff

    return None  # Not reached due to the raise

# Example usage:
#if __name__ == '__main__':
#    try:
#        data = retry_request('https://api.example.com/data')
#        print(data)
#    except RetryException as e:
#        print(e)