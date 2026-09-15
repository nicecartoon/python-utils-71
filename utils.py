import time
import functools
import logging

logger = logging.getLogger('python-utils-71')

def retry_network_op(attempts=3, delay=1.0, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries, current_delay = attempts, delay
            while tries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries -= 1
                    if tries == 0:
                        logger.error(f'operation failed after {attempts} attempts')
                        raise e
                    logger.warning(f'retry {attempts - tries} due to {e}')
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class ConnectionChaos:
    def __init__(self, fail_rate=0.5):
        self.fail_rate = fail_rate

    def __call__(self, func):
        import random
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if random.random() < self.fail_rate:
                raise ConnectionError('simulated network instability')
            return func(*args, **kwargs)
        return wrapper