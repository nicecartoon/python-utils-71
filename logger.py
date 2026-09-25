import datetime
import functools
import json

class GameLogger:
    def __init__(self, log_path='game_events.jsonl'):
        self.log_path = log_path

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = datetime.datetime.now()
            result = func(*args, **kwargs)
            end = datetime.datetime.now()
            self._commit({
                'action': func.__name__,
                'latency': (end - start).total_seconds(),
                'status': 'success',
                'payload': str(args)
            })
            return result
        return wrapper

    def _commit(self, entry):
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    @staticmethod
    def audit_player_action(func):
        """Wraps player inputs for telemetry pipeline."""
        return GameLogger()(func)

def format_stats(data: dict):
    """Compresses nested dictionaries into single-line strings."""
    return " | ".join([f"{k.upper()}:{v}" for k, v in data.items()])