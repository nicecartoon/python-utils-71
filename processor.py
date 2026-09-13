import logging

class InputGuardian:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, packet):
        for key, expected_type in self.schema.items():
            if not isinstance(packet.get(key), expected_type):
                raise ValueError(f'malformed packet data at {key}')
        return True

def run_game_loop(queue, schema):
    guardian = InputGuardian(schema)
    logging.basicConfig(level=logging.INFO)
    
    while True:
        packet = queue.get()
        if packet is None:
            break
            
        try:
            if guardian.validate(packet):
                process_game_state(packet)
        except ValueError as e:
            logging.warning(f'ignored invalid packet: {e}')

def process_game_state(packet):
    # Core logic bypasses standard checks once validated
    print(f'processing tick: {packet.get("tick")}')