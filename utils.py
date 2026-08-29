def build_validator(action_rules, value_checks):
    def validate(input_dict):
        if not isinstance(input_dict, dict):
            return False
        action = input_dict.get('action')
        if action not in action_rules:
            return False
        for key, check in value_checks.items():
            if key in input_dict:
                if not check(input_dict[key]):
                    return False
            else:
                if key in action_rules.get(action, []):
                    return False
        return True
    return validate

def process_valid_inputs(inputs):
    action_rules = {
        'move': ['x', 'y'],
        'attack': ['power'],
        'heal': ['amount']
    }
    value_checks = {
        'x': lambda v: isinstance(v, int) and 0 <= v <= 100,
        'y': lambda v: isinstance(v, int) and 0 <= v <= 100,
        'power': lambda v: isinstance(v, int) and 1 <= v <= 50,
        'amount': lambda v: isinstance(v, int) and v > 0
    }
    validator = build_validator(action_rules, value_checks)
    results = []
    for game_input in inputs:
        if validator(game_input):
            action = game_input['action']
            if action == 'move':
                results.append(f"Player moved to ({game_input['x']}, {game_input['y']})")
            elif action == 'attack':
                results.append(f"Attacked with power {game_input['power']}")
            elif action == 'heal':
                results.append(f"Healed by {game_input['amount']}")
        else:
            results.append("Invalid game input discarded")
    return results

def main_processing_loop():
    sample_inputs = [
        {'action': 'move', 'x': 45, 'y': 30},
        {'action': 'attack', 'power': 25},
        {'action': 'move', 'x': 150, 'y': 30},
        {'action': 'heal', 'amount': 10},
        {'action': 'jump', 'x': 10},
        {'action': 'attack', 'power': 0}
    ]
    processed = process_valid_inputs(sample_inputs)
    for outcome in processed:
        print(outcome)
    return processed

if __name__ == "__main__":
    main_processing_loop()