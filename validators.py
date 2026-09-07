import time
from typing import Generator, Dict, Any, Tuple

def create_input_validator(min_delay: float = 0.05) -> Generator[Tuple[bool, str], Dict[str, Any], None]:
    """
    Creates a stateful game input validator using a coroutine.
    Validates input rates, screen space coordinates, and key mappings.
    """
    last_time: float = 0.0
    allowed_keys = {"up", "down", "left", "right", "action_a", "action_b"}
    
    # Prime generator
    payload = yield (True, "ready")
    
    while payload is not None:
        now = payload.get("timestamp", time.time())
        key = payload.get("key", "")
        coords = payload.get("coords", (0, 0))
        
        if now - last_time < min_delay:
            payload = yield (False, "rate limit triggered")
            continue
            
        if key not in allowed_keys:
            payload = yield (False, f"unsupported key mapping: {key}")
            continue
            
        # Check viewport bounds (assuming a 1920x1080 engine viewport)
        if "coords" in payload:
            x, y = coords
            if not (0 <= x <= 1920 and 0 <= y <= 1080):
                payload = yield (False, f"out of bounds coordinates: {x},{y}")
                continue
                
        last_time = now
        payload = yield (True, "valid")