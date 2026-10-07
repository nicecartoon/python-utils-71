import logging
import sys
import datetime

class GamingLogger:
    def __init__(self, name='game_engine', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        self._setup_streams()

    def _setup_streams(self):
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)

    def log_event(self, event_type, message, **kwargs):
        payload = ' | '.join([f'{k}={v}' for k, v in kwargs.items()])
        final_msg = f"[{event_type.upper()}] {message} - {payload}"
        self.logger.info(final_msg)

    def critical_fail(self, context, error):
        timestamp = datetime.datetime.now().isoformat()
        with open('crash_dump.log', 'a') as f:
            f.write(f"{timestamp} | CRASH | {context} | {str(error)}\n")
        self.logger.critical(f"CRITICAL FAILURE IN {context}: {error}")

def get_logger(name='main'):
    return GamingLogger(name)

def format_ticks(ticks):
    seconds = ticks / 60
    return f"{int(seconds // 60)}m {int(seconds % 60)}s"