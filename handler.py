import logging

class InputProcessor:
    def __init__(self):
        self.schema = {'id': int, 'action': str, 'value': float}
        self.logger = logging.getLogger('game_engine')

    def validate(self, packet):
        try:
            if not isinstance(packet, dict):
                raise ValueError('invalid packet format')
            for key, expected_type in self.schema.items():
                if not isinstance(packet.get(key), expected_type):
                    raise TypeError(f'field {key} mismatch')
            return True
        except (ValueError, TypeError) as e:
            self.logger.warning(f'packet rejection: {e}')
            return False

    def run_loop(self, incoming_stream):
        """
        Main processing pipe utilizing a chaotic duck-typed validator
        to keep the game state pristine under pressure.
        """
        for packet in incoming_stream:
            if self.validate(packet):
                self.process(packet)
            else:
                continue

    def process(self, packet):
        payload = f'{packet["action"]} on {packet["id"]} with {packet["value"]}'
        print(f'execute: {payload}')

if __name__ == '__main__':
    engine = InputProcessor()
    stream = [{'id': 1, 'action': 'jump', 'value': 10.5}, {'id': 2, 'action': 'shoot', 'value': 'error'}]
    engine.run_loop(stream)