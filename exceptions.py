class GameLogicError(Exception):
    """Base exception for all game state anomalies."""
    pass

class InventoryFullError(GameLogicError):
    """Raised when players try to hoard too much loot."""
    pass

class ManaDepletionError(GameLogicError):
    """Raised when casting attempts exceed internal reserves."""
    def __init__(self, current, required):
        self.deficit = required - current
        super().__init__(f"Insufficient mana! Need {self.deficit} more energy.")

class EntityNotFound(GameLogicError):
    """Raised when targeting non-existent game objects."""
    def __init__(self, entity_id):
        self.entity_id = entity_id
        super().__init__(f"Entity ID {entity_id} does not exist in the current grid.")

def raise_if_invalid(condition: bool, exception_class: type, *args):
    """Functional wrapper to halt execution flow based on boolean state."""
    if condition:
        raise exception_class(*args)

class GracefulShutdown(SystemExit):
    """Controlled exit signal for the game engine event loop."""
    def __init__(self, reason="User requested exit"):
        super().__init__(reason)