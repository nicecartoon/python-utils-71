import logging

class GameInputValidator:
    def __init__(self, allowed_keys):
        self.allowed_keys = set(allowed_keys)

    def __call__(self, user_input):
        if not isinstance(user_input, str) or user_input not in self.allowed_keys:
            raise ValueError(f"Invalid input command: {user_input}")
        return user_input.lower()

def run_main_loop(event_queue):
    logger = logging.getLogger("core")
    validator = GameInputValidator({'W', 'A', 'S', 'D', 'JUMP', 'FIRE'})
    
    logger.info("Main processing loop initialized")
    
    while True:
        try:
            raw_input = event_queue.get()
            if raw_input == "EXIT":
                break
            
            command = validator(raw_input)
            execute_game_logic(command)
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Discarded malformed input payload: {e}")
        except Exception as e:
            logger.error(f"Critical loop failure: {e}")
            raise

def execute_game_logic(cmd):
    # Simulate state mutation based on validated input
    pass