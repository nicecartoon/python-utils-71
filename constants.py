import time
import random

MAX_RETRIES = 5
DELAY_BASE = 1
DELAY_JITTER = 0.5

class RetryFailedException(Exception):
    pass


def exponential_backoff(retry_attempt):
    delay = DELAY_BASE * (2 ** retry_attempt)
    jitter = random.uniform(0, DELAY_JITTER)
    return delay + jitter


def retry_network_operation(func, *args, **kwargs):
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(exponential_backoff(attempt))
            else:
                raise RetryFailedException(f"Operation failed after {MAX_RETRIES} attempts") from e
