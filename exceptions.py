"""Custom exceptions for gaming data handling."""

class GamingDataError(Exception):
    def __init__(self, message, game_id=None, player_id=None):
        super().__init__(message)
        self.game_id = game_id
        self.player_id = player_id

    def get_context(self):
        return {"game_id": self.game_id, "player_id": self.player_id}

class InvalidDataFormatError(GamingDataError):
    def __init__(self, message, expected_format, **kwargs):
        super().__init__(message, **kwargs)
        self.expected_format = expected_format

    def suggest_fix(self):
        return f"Use {self.expected_format} format"

class MissingFieldError(GamingDataError):
    def __init__(self, field, **kwargs):
        super().__init__(f"Missing '{field}'", **kwargs)
        self.field = field

class CorruptedGameDataError(GamingDataError):
    def attempt_recovery(self, default_data):
        print("Using default data for recovery")
        return default_data

class ScoreOverflowError(GamingDataError):
    def __init__(self, message, max_allowed, **kwargs):
        super().__init__(message, **kwargs)
        self.max_allowed = max_allowed

    def normalize_score(self, score):
        return min(score, self.max_allowed)

def validate_gaming_data(data):
    if data is None or not isinstance(data, dict):
        raise InvalidDataFormatError("Invalid gaming data type", "dict")
    for field in ["player_id", "game_id", "stats"]:
        if field not in data:
            raise MissingFieldError(field, game_id=data.get("game_id"), player_id=data.get("player_id"))
    if not isinstance(data["stats"], dict):
        raise InvalidDataFormatError("Stats not dict", "dict", game_id=data["game_id"], player_id=data["player_id"])
    if data.get("level", 0) < 0:
        raise GamingDataError("Negative level", game_id=data["game_id"], player_id=data["player_id"])
    return True

def handle_gaming_data(raw_data):
    try:
        if validate_gaming_data(raw_data):
            data = raw_data.copy()
            if data.get("score", 0) > 10000:
                raise ScoreOverflowError("Overflow", 10000, game_id=data["game_id"], player_id=data["player_id"])
            data["processed"] = True
            return data
    except GamingDataError as e:
        ctx = e.get_context()
        fallback = {"player_id": ctx.get("player_id", "unknown"), "game_id": ctx.get("game_id", "unknown"), "stats": {}, "error": str(e)}
        if isinstance(e, CorruptedGameDataError):
            fallback = e.attempt_recovery(fallback)
        return fallback
    return raw_data