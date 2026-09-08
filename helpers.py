import functools

def validate_game_input(expected_types):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            params = dict(zip(func.__code__.co_varnames, args))
            params.update(kwargs)
            for key, expected_type in expected_types.items():
                if key in params and not isinstance(params[key], expected_type):
                    raise TypeError(f'expected {expected_type} for {key}, got {type(params[key])}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

class InputSanitizer:
    @staticmethod
    def sanitize_coords(data):
        if not isinstance(data, (list, tuple)) or len(data) != 2:
            return (0, 0)
        return tuple(int(max(0, min(1024, x))) for x in data)

def main_processing_loop(event_stream):
    for event in event_stream:
        try:
            action = event.get('type')
            payload = event.get('data')
            if action == 'move':
                coords = InputSanitizer.sanitize_coords(payload)
                print(f'moving player to {coords}')
            else:
                print(f'unknown event {action}')
        except Exception as e:
            print(f'dropped malformed event: {e}')