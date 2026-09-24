import time
import threading
from collections import deque

class AsyncBufferLogger:
    def __init__(self, capacity=1024):
        self._buffer = deque(maxlen=capacity)
        self._lock = threading.Lock()
        self._flush_interval = 2.0
        self._running = True
        threading.Thread(target=self._periodic_flush, daemon=True).start()

    def log(self, message: str):
        ts = time.perf_counter()
        self._buffer.append(f'[{ts:.4f}] {message}')

    def _periodic_flush(self):
        while self._running:
            time.sleep(self._flush_interval)
            self._drain()

    def _drain(self):
        if not self._buffer:
            return
        with self._lock:
            batch = list(self._buffer)
            self._buffer.clear()
            # Direct I/O optimization: bypass print for bulk binary write simulation
            try:
                with open('game_debug.log', 'a') as f:
                    f.write('\n'.join(batch) + '\n')
            except IOError:
                pass

    def shutdown(self):
        self._running = False
        self._drain()

# Singleton instance for high-frequency game events
logger = AsyncBufferLogger()