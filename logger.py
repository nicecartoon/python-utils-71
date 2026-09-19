import logging
import functools
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('python-utils-71')

def validate_input(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        data = args[0] if args else kwargs.get('data')
        if not isinstance(data, (dict, list)):
            logger.error(f'invalid input schema: {type(data).__name__}')
            return None
        return func(*args, **kwargs)
    return wrapper

class GameProcessor:
    def __init__(self):
        self.active = True

    @validate_input
    def process_tick(self, data: Any) -> None:
        logger.info(f'processing game tick: {data}')

    def run_loop(self, queue: list) -> None:
        for item in queue:
            if not self.active:
                break
            self.process_tick(item)

if __name__ == '__main__':
    engine = GameProcessor()
    input_stream = [{'cmd': 'move', 'val': 10}, 'malformed_data', {'cmd': 'jump'}]
    engine.run_loop(input_stream)