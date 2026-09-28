import logging
from typing import Any, Dict, Optional

class GameStateError(Exception):
    pass

class DataProcessor:
    def __init__(self, debug_mode: bool = False):
        self.debug = debug_mode
        self.logger = logging.getLogger('processor')

    def sanitize_input(self, payload: Any) -> Dict[str, Any]:
        try:
            if not isinstance(payload, dict):
                raise GameStateError(f"Expected dict, received {type(payload).__name__}")
            
            return {
                'id': payload.get('id', 'unknown'),
                'score': int(payload.get('score', 0)),
                'status': str(payload.get('status', 'idle'))
            }
        except (ValueError, TypeError) as e:
            self.logger.error(f"Sanitization failure: {e}")
            return {'error': True, 'msg': 'Malformed packet structure'}

    def process_frame(self, frame_data: Any) -> Optional[Dict[str, Any]]:
        clean_data = self.sanitize_input(frame_data)
        
        if clean_data.get('error'):
            return None
            
        if clean_data['score'] < 0:
            self.logger.warning(f"Negative score detected: {clean_data['score']}")
            clean_data['score'] = 0
            
        return clean_data

def run_safe_process(data: Any):
    proc = DataProcessor(debug_mode=True)
    result = proc.process_frame(data)
    return result or {'status': 'discarded'}