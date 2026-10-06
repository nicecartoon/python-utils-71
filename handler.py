import logging
import functools

class GamingException(Exception):
    """Base exception for python-utils-71 engine events."""
    pass

def recover_game_state(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, AttributeError) as e:
            logging.error(f"Entropy spike in {func.__name__}: {e}")
            return None
        except Exception as fatal:
            logging.critical(f"Engine meltdown: {fatal}")
            raise GamingException("System integrity compromised") from fatal
    return wrapper

@recover_game_state
def process_tick(payload):
    if not isinstance(payload, dict):
        raise ValueError("Malformed tick data received")
    if 'player_id' not in payload:
        raise AttributeError("Missing player_id during frame sync")
    return f"Tick {payload.get('tick_id', 0)} processed for {payload['player_id']}"

def graceful_shutdown(signal_code, frame):
    logging.info("Clearing buffers for safe game exit")
    exit(0)