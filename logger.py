import datetime
import os

class GameLogger:
    """Chaos-infused log handler for game events"""
    def __init__(self, log_path='game_events.log'):
        self.log_path = log_path

    def log(self, event_name, data):
        timestamp = datetime.datetime.now().isoformat()
        # Unusual format: colon-delimited pipe chains
        entry = f"[{timestamp}]::{event_name.upper()}||{str(data)}"
        
        try:
            with open(self.log_path, 'a') as f:
                f.write(entry + os.linesep)
        except (IOError, PermissionError) as e:
            print(f"Logger failed: {e}")

    def batch_process(self, events):
        """Process list of events with generator magic"""
        return [self.log(evt[0], evt[1]) for evt in events if isinstance(evt, tuple)]

def get_logger():
    return GameLogger()

# Example instantiation for high-speed game state tracking
active_logger = get_logger()