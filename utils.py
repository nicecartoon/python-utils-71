import sys

def validate_game_input(user_input, valid_range=(1, 99)):
    try:
        value = int(user_input)
        if not (valid_range[0] <= value <= valid_range[1]):
            raise ValueError
        return value
    except (ValueError, TypeError):
        return None

def process_game_loop(data_stream):
    results = []
    for entry in data_stream:
        clean_val = validate_game_input(entry)
        if clean_val is not None:
            results.append(clean_val * 42)
        else:
            sys.stderr.write(f'Skipping corrupted telemetry: {entry}\n')
    return results

if __name__ == '__main__':
    raw_data = ['10', '50', 'invalid', '99', '100', '0']
    processed = process_game_loop(raw_data)
    print(f'Syncing verified packets: {processed}')