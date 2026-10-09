import re
from typing import Callable, List, Dict

class GameValidator:
    def __init__(self, predicate: Callable[[List[str]], bool], error_msg: str):
        self.predicate = predicate
        self.error_msg = error_msg

    def __and__(self, other: "GameValidator") -> "GameValidator":
        return GameValidator(
            lambda tokens: self.predicate(tokens) and other.predicate(tokens),
            f"{self.error_msg} AND {other.error_msg}"
        )

def is_action(action: str) -> GameValidator:
    return GameValidator(lambda t: len(t) > 0 and t[0].upper() == action.upper(), f"must start with {action}")

def arg_count(count: int) -> GameValidator:
    return GameValidator(lambda t: len(t) == count, f"must have exactly {count} parts")

def numeric_arg(index: int) -> GameValidator:
    def check(t: List[str]) -> bool:
        return index < len(t) and t[index].isdigit()
    return GameValidator(check, f"parameter at index {index} must be numeric")

class GameLoopProcessor:
    def __init__(self):
        self.rules = {
            "MOVE": is_action("MOVE") & arg_count(2),
            "CAST": is_action("CAST") & arg_count(3) & numeric_arg(2),
            "EQUIP": is_action("EQUIP") & arg_count(2)
        }

    def process_commands(self, raw_inputs: List[str]) -> List[str]:
        output_logs = []
        for raw in raw_inputs:
            clean = re.sub(r'[^\w\s]', '', raw).strip()
            if not clean:
                output_logs.append("skipped empty action")
                continue
            tokens = clean.split()
            verb = tokens[0].upper()
            rule = self.rules.get(verb)
            if not rule:
                output_logs.append(f"failed validation: unknown action '{verb}'")
                continue
            if rule.predicate(tokens):
                output_logs.append(f"processed action {verb} with args {tokens[1:]}")
            else:
                output_logs.append(f"failed validation: {rule.error_msg}")
        return output_logs