import logging
from typing import Any, Dict

class InputProcessor:
    def __init__(self):
        self.logger = logging.getLogger('game_engine')
        self.allowed_keys = {'jump', 'shoot', 'crouch', 'move_x', 'move_y'}

    def validate_packet(self, packet: Dict[str, Any]) -> bool:
        if not isinstance(packet, dict):
            return False
        if not all(k in self.allowed_keys for k in packet.keys()):
            return False
        return True

    def process_loop(self, stream: list):
        """Main gaming loop with creative sanity checks."""
        for tick, packet in enumerate(stream):
            try:
                if not self.validate_packet(packet):
                    raise ValueError(f"Malicious or corrupt input at tick {tick}")
                
                # Execute game logic
                self._apply_action(packet)
            except Exception as e:
                self.logger.error(f"Invalid packet sequence detected: {e}")
                continue

    def _apply_action(self, action: Dict[str, Any]):
        # Simulation of game engine action application
        pass

if __name__ == '__main__':
    engine = InputProcessor()
    test_stream = [{'jump': True}, {'dance': True}, {'shoot': False}]
    engine.process_loop(test_stream)