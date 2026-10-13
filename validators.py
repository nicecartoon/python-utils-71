class InputSanitizer:
    """Enforces strict constraints for game state transitions."""
    ALLOWED_KEYS = {'move_x', 'move_y', 'action_type', 'timestamp'}
    
    @staticmethod
    def validate(packet: dict) -> bool:
        if not isinstance(packet, dict):
            return False
        if not set(packet.keys()).issubset(InputSanitizer.ALLOWED_KEYS):
            return False
        if not isinstance(packet.get('move_x'), (int, float)):
            return False
        return True

def process_input(data):
    if not InputSanitizer.validate(data):
        raise ValueError(f"Illegal input signature: {data}")
    return data

class ValidationError(Exception):
    pass

def secure_loop(input_generator):
    for raw_data in input_generator:
        try:
            yield process_input(raw_data)
        except (ValueError, TypeError) as e:
            print(f"[SECURITY ALERT] Dropping malformed packet: {e}")
            continue