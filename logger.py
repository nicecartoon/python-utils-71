import sys
import functools
import traceback

def robust_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_id = hex(hash(str(e)))
            sys.stderr.write(f'[GAMING-CRITICAL] [{err_id}] - {type(e).__name__}: {str(e)}\n')
            if 'Critical' in type(e).__name__:
                sys.exit(1)
            return None
    return wrapper

class GameLogger:
    def __init__(self, mode='verbose'):
        self.mode = mode

    @robust_log
    def log_event(self, msg: str):
        if not isinstance(msg, str):
            raise ValueError('Non-string log entry provided')
        print(f'>> {msg.upper()}')

    @robust_log
    def dump_state(self, data: dict):
        if not data:
            raise KeyError('State dump requires non-empty data')
        print(f'Dumping {len(data)} keys to buffer...')

if __name__ == '__main__':
    logger = GameLogger()
    logger.log_event('init_engine')
    logger.log_event(None)
    logger.dump_state({})
    logger.dump_state({'player': 'hero', 'hp': 100})