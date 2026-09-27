from enum import IntFlag, auto
from typing import Any, Dict, List


class FaultSeverity(IntFlag):
    """Bitmask flags specifying operational impact of game faults."""

    MINOR = auto()
    GRAPHICAL = auto()
    STATE_CORRUPTION = auto()
    CRITICAL = auto()


class GameEngineError(Exception):
    """Base exception class for game runtime failures with telemetry context.

    Attributes:
        message: Primary human-readable exception summary.
        severity: Bitmask indicating error impact level.
        context: State payload parameters captured at failure time.
    """

    def __init__(
        self,
        message: str,
        severity: FaultSeverity = FaultSeverity.MINOR,
        **context: Any
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.severity: FaultSeverity = severity
        self.context: Dict[str, Any] = context

    def telemetry_dump(self) -> Dict[str, Any]:
        """Formats exception context into structured telemetry payload.

        Returns:
            Dict[str, Any]: Dictionary ready for analytics emission.
        """
        active_flags: List[str] = [
            flag.name for flag in FaultSeverity if flag in self.severity and flag.name
        ]
        return {
            "fault_type": self.__class__.__name__,
            "severity_code": int(self.severity),
            "severity_flags": active_flags,
            "summary": self.message,
            "payload": self.context,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"severity={self.severity!r}, context={self.context!r})"
        )


class InventoryFullError(GameEngineError):
    """Raised when item acquisition exceeds inventory capacity constraints."""

    def __init__(
        self,
        item_id: str,
        current_slots: int,
        max_slots: int,
        severity: FaultSeverity = FaultSeverity.MINOR
    ) -> None:
        msg: str = f"Inventory breach: item '{item_id}' rejected ({current_slots}/{max_slots})"
        super().__init__(
            msg,
            severity=severity,
            item_id=item_id,
            current_slots=current_slots,
            max_slots=max_slots
        )


class OutOfManaError(GameEngineError):
    """Raised when spell casting cost exceeds available energy resource."""

    def __init__(
        self,
        spell_id: str,
        required_mana: float,
        available_mana: float
    ) -> None:
        deficit: float = required_mana - available_mana
        sev: FaultSeverity = FaultSeverity.STATE_CORRUPTION if deficit > 1000.0 else FaultSeverity.MINOR
        msg: str = f"Cast fail for '{spell_id}': short by {deficit:.1f} mana"
        super().__init__(
            msg,
            severity=sev,
            spell_id=spell_id,
            required=required_mana,
            available=available_mana,
            deficit=deficit
        )
