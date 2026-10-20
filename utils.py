import sys

def validate_game_input(user_input):
    """Sanitizes and validates game-specific command strings."""
    allowed_commands = {'jump', 'fire', 'duck', 'run'}
    try:
        command = str(user_input).strip().lower()
        if command not in allowed_commands:
            raise ValueError(f"Illegal move: {command}")
        return command
    except Exception as e:
        return None

def process_game_loop():
    """Execution loop with strict input gatekeeping."""
    print("Gaming Engine: Ready. (Enter command or exit)")
    while True:
        raw_data = sys.stdin.readline()
        if not raw_data or raw_data.strip().lower() == 'exit':
            break
            
        clean_cmd = validate_game_input(raw_data)
        if clean_cmd:
            print(f"Executing {clean_cmd.upper()} action...")
        else:
            print("Input glitch detected: command ignored")

if __name__ == '__main__':
    process_game_loop()