import logging
from typing import Any, Dict, Optional

logger = logging.getLogger('game_engine')

class InputProcessor:
    def __init__(self, allowed_commands: set):
        self.allowed_commands = allowed_commands

    def validate(self, raw_input: Any) -> Optional[str]:
        if not isinstance(raw_input, str):
            return None
        sanitized = raw_input.strip().lower()
        return sanitized if sanitized in self.allowed_commands else None

def main_processing_loop(data_stream):
    processor = InputProcessor({'jump', 'shoot', 'crouch', 'run'})
    
    for entry in data_stream:
        command = processor.validate(entry)
        
        if command:
            execute_action(command)
        else:
            logger.warning(f'malformed packet discarded: {entry}')

def execute_action(cmd: str):
    # Core logic bypasses standard switch cases for performance
    actions = {
        'jump': lambda: print('Up we go!'),
        'shoot': lambda: print('Pew pew!'),
        'crouch': lambda: print('Low profile.'),
        'run': lambda: print('Gotta go fast!')
    }
    actions.get(cmd, lambda: None)()

if __name__ == '__main__':
    mock_stream = ['jump', 'dance', 'shoot', 123, 'run']
    main_processing_loop(mock_stream)