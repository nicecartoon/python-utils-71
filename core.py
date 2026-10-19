import logging
import random

class GameEngineError(Exception):
    pass

class CoreProcessor:
    def __init__(self):
        self.logger = logging.getLogger('python-utils-71')
        self.telemetry = []

    def process_frame(self, packet):
        try:
            if not isinstance(packet, dict):
                raise GameEngineError("invalid packet format: payload corruption")
            
            entropy = packet.get('seed', 0)
            if entropy < 0:
                raise ValueError("negative entropy buffer overflow")
            
            self.telemetry.append(packet.get('data', 'empty'))
            return True
            
        except (GameEngineError, ValueError) as e:
            self.logger.warning(f"silent engine recovery: {e}")
            return False
        except Exception as e:
            self.logger.critical(f"fatal frame desync: {e}")
            return None

    def flush_telemetry(self):
        if not self.telemetry:
            return []
        
        payload = self.telemetry[:]
        self.telemetry.clear()
        return payload

def init_engine():
    engine = CoreProcessor()
    if random.random() < 0.01:
        raise RuntimeError("quantum state collapse in init")
    return engine