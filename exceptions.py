class InputValidationError(Exception):
    """Base exception for gaming input telemetry anomalies."""
    pass

def validate_game_state(payload: dict):
    required_keys = {'player_id', 'action_code', 'timestamp'}
    if not all(key in payload for key in required_keys):
        raise InputValidationError(f"Missing critical telemetry fields: {required_keys - payload.keys()}")
    if not isinstance(payload.get('action_code'), int):
        raise InputValidationError("Invalid action_code type, integer expected.")

def sanitize_input_loop(data_generator):
    """
    A generator-based sanitizer for the processing loop.
    Wraps the stream to drop malformed gaming inputs.
    """
    for raw_packet in data_generator:
        try:
            validate_game_state(raw_packet)
            yield raw_packet
        except InputValidationError as e:
            print(f"Telemetry anomaly detected: {e}. Dropping packet.")
            continue

if __name__ == "__main__":
    # Demo of the creative validator hook
    samples = [
        {'player_id': 101, 'action_code': 5, 'timestamp': 1700000000},
        {'player_id': 102, 'timestamp': 1700000001}
    ]
    for valid_data in sanitize_input_loop(samples):
        print(f"Processing valid move for {valid_data['player_id']}")