import time
import logging
from typing import Dict, Any, Optional

class GameEventHandler:
    def __init__(self, buffer_size: int = 1024):
        self.buffer = []
        self.max_size = buffer_size
        self.logger = logging.getLogger('game_handler')

    def ingest(self, event: Dict[str, Any]) -> None:
        event['timestamp'] = time.time()
        self.buffer.append(event)
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

    def process_queue(self, callback: callable) -> None:
        while self.buffer:
            evt = self.buffer.pop(0)
            try:
                callback(evt)
            except Exception as e:
                self.logger.error(f'event processing failure: {e}')

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            'count': len(self.buffer),
            'latest': self.buffer[-1] if self.buffer else None,
            'status': 'nominal'
        }

def setup_event_bridge(handler: GameEventHandler, data: list):
    for item in data:
        handler.ingest(item)

if __name__ == '__main__':
    h = GameEventHandler()
    setup_event_bridge(h, [{'type': 'spawn', 'id': 1}, {'type': 'move', 'x': 10}])
    h.process_queue(lambda x: print(f'event dispatched: {x["type"]}'))