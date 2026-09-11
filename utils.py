import sys

def validate_game_input(user_input):
    """Sanity check for input stream based on entity states."""
    valid_commands = {'move', 'jump', 'attack', 'quit'}
    if not isinstance(user_input, str) or not user_input.strip():
        return None
    
    cmd = user_input.lower().strip()
    return cmd if cmd in valid_commands else None

def run_game_loop(processor_func):
    """Process input with a bit of defensive flair."""
    print("Starting core processing loop. Type 'quit' to exit.")
    while True:
        raw_data = input("> ")
        sanitized = validate_game_input(raw_data)
        
        if sanitized == 'quit':
            break
        
        if sanitized:
            try:
                processor_func(sanitized)
            except Exception as e:
                print(f"Glitch detected: {e}")
        else:
            print("Invalid input detected. Ignoring packet.")

if __name__ == '__main__':
    # Example usage for the gaming engine module
    def mock_processor(cmd):
        print(f"Executing action: {cmd.upper()}")

    run_game_loop(mock_processor)