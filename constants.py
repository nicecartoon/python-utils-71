import time
import random

class RetryConfig:
    def __init__(self, max_attempts=5, base_delay=1.0, backoff_factor=2, jitter=True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

    def get_delay(self, attempt):
        delay = self.base_delay * (self.backoff_factor ** attempt)
        if self.jitter:
            delay += random.uniform(0, 1)
        return delay

RETRY_CONFIG = RetryConfig(max_attempts=5, base_delay=1.0, backoff_factor=2, jitter=True)