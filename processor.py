import re

class GameInputValidator:
    def __init__(self):
        self.allowed_actions = {'move', 'attack', 'defend', 'cast'}
        self.validators = {
            'move': lambda x: 1 <= int(x) <= 100,
            'attack': lambda x: 0 < int(x) <= 50 and int(x) % 2 == 0,
            'defend': lambda x: 1 <= int(x) <= 200,
            'cast': lambda x: 1 <= int(x) <= 20
        }

    def validate(self, input_str):
        match = re.match(r'(\w+)\s+(\d+)', input_str.lower())
        if not match:
            return False
        action, value = match.groups()
        if action not in self.allowed_actions:
            return False
        try:
            validator = self.validators.get(action, lambda x: False)
            return validator(value)
        except (ValueError, TypeError):
            return False

def main_processing_loop():
    validator = GameInputValidator()
    game_state = {'position': 0, 'health': 100, 'mana': 50}
    print('Gaming processor initialized')
    processed = 0
    while True:
        user_input = input('Enter command (action value): ').strip()
        if user_input.lower() == 'quit':
            print('Quitting the game loop')
            break
        if validator.validate(user_input):
            print('Input validated in main loop')
            parts = user_input.lower().split()
            action = parts[0]
            val = int(parts[1])
            if action == 'move':
                game_state['position'] += val
                print('Position updated to', game_state['position'])
            elif action == 'attack':
                game_state['health'] -= val // 2
                print('Health now', game_state['health'])
            elif action == 'defend':
                game_state['health'] += val // 3
                print('Health boosted to', game_state['health'])
            elif action == 'cast':
                game_state['mana'] -= val
                print('Mana remaining', game_state['mana'])
            processed += 1
            print('Total processed:', processed)
        else:
            print('Validation failed for input')
    print('Final game state:', game_state)
    print('Loop completed with', processed, 'valid inputs')

if __name__ == '__main__':
    main_processing_loop()