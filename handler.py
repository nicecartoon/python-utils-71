import time
import collections
from typing import Dict, Any, Callable

class GameEventHandler:
    def __init__(self):
        self._registry = collections.defaultdict(list)
        self._history = collections.deque(maxlen=100)

    def subscribe(self, event_type: str, callback: Callable):
        self._registry[event_type].append(callback)

    def emit(self, event_type: str, payload: Dict[str, Any]):
        timestamp = time.time()
        entry = {'type': event_type, 'data': payload, 'time': timestamp}
        self._history.append(entry)
        
        for callback in self._registry.get(event_type, []):
            try:
                callback(payload)
            except Exception as e:
                print(f'Critical failure in handler {callback}: {e}')

    def get_event_stats(self) -> Dict[str, int]:
        stats = collections.Counter(e['type'] for e in self._history)
        return dict(stats)

    def flush_stale_events(self, threshold: float = 3600.0):
        now = time.time()
        while self._history and (now - self._history[0]['time']) > threshold:
            self._history.popleft()

    def __repr__(self):
        return f'<GameEventHandler registry_size={len(self._registry)}>'