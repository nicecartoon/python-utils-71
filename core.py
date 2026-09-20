import sys
from typing import Generator, Any, Dict, Callable

class GameInputError(ValueError):
    """Custom exception raised when player input validation fails."""
    pass

def validate_schema(schema: Dict[str, type]) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(payload: Dict[str, Any]) -> Any:
            for key, expected_type in schema.items():
                if key not in payload:
                    raise GameInputError(f"Missing field: {key}")
                if not isinstance(payload[key], expected_type):
                    raise GameInputError(f"Invalid type for {key}: expected {expected_type.__name__}")
            return func(payload)
        return wrapper
    return decorator

class InputPipeline:
    def __init__(self) -> None:
        self.allowed_actions = {"MOVE_LEFT", "MOVE_RIGHT", "JUMP", "ATTACK", "CAST_SPELL"}

    @validate_schema({"player_id": int, "action": str, "frame_id": int})
    def validate_frame(self, frame: Dict[str, Any]) -> Dict[str, Any]:
        if frame["action"] not in self.allowed_actions:
            raise GameInputError(f"Illegal action: {frame['action']}")
        return frame

    def process_loop(self, raw_frames: list[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for frame in raw_frames:
            try:
                yield self.validate_frame(frame)
            except GameInputError as err:
                sys.stderr.write(f"[FRAME REJECTED] {err}\n")

if __name__ == "__main__":
    pipeline = InputPipeline()
    sample_input = [
        {"player_id": 1, "action": "JUMP", "frame_id": 101},
        {"player_id": 2, "action": "FLY", "frame_id": 102},
        {"player_id": "3", "action": "ATTACK", "frame_id": 103},
        {"player_id": 4, "action": "CAST_SPELL", "frame_id": 104},
    ]
    valid_events = list(pipeline.process_loop(sample_input))
    print(f"Validated {len(valid_events)} game frames successfully.")