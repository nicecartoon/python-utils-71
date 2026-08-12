import json
import os
import datetime

class GameLogger:
    def __init__(self, game_name):
        self.game_name = game_name
        self.log_file = f'{game_name}_log.json'
        self.logs = []
        self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                self.logs = json.load(file)

    def log_event(self, event_type, message):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {'timestamp': timestamp, 'event_type': event_type, 'message': message}
        self.logs.append(log_entry)
        self.save_logs()

    def save_logs(self):
        with open(self.log_file, 'w') as file:
            json.dump(self.logs, file, indent=4)

    def get_logs(self):
        return self.logs

logger = GameLogger('MyCoolGame')

logger.log_event('INFO', 'Game started!')
logger.log_event('ERROR', 'An unexpected error occurred.')
