import time
import collections
from typing import Any, Callable, Dict

class GameEventStream:
    def __init__(self):
        self._buffer = collections.deque(maxlen=128)
        self._registry: Dict[str, Callable] = {}

    def subscribe(self, event_type: str, callback: Callable):
        self._registry[event_type] = callback

    def emit(self, event_type: str, data: Any):
        packet = {'type': event_type, 'payload': data, 'ts': time.time()}
        self._buffer.append(packet)
        if event_type in self._registry:
            self._registry[event_type](data)

    def flush(self) -> list:
        items = list(self._buffer)
        self._buffer.clear()
        return items

def create_event_handler():
    handler = GameEventStream()
    
    def logger(data):
        print(f'[EVENT LOG] {data}')
    
    handler.subscribe('player_join', logger)
    handler.subscribe('combat_start', lambda d: print(f'Initiating {d}'))
    return handler

if __name__ == '__main__':
    instance = create_event_handler()
    instance.emit('player_join', {'id': 'P1', 'pos': (0, 0)})
    instance.emit('combat_start', 'Arena_Alpha')