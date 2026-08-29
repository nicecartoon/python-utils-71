import random
from typing import Dict, Any

class GameHandler:
    """Handles game events with creative error recovery for edge cases"""

    def __init__(self):
        self.state = {"players": {}, "scores": {}}
        self.history = []

    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not isinstance(event, dict):
                raise ValueError("Event must be dictionary")
            if "type" not in event:
                raise KeyError("Event type required")
            event_type = event["type"]
            if event_type == "join":
                player = event.get("player", "")
                if not isinstance(player, str) or not player:
                    raise ValueError("Player name must be non-empty string")
                if player in self.state["players"]:
                    raise ValueError("Player already in game")
                self.state["players"][player] = {"active": True}
                self.state["scores"][player] = 100
                self.history.append(f"join:{player}")
                return {"status": "joined", "player": player}
            elif event_type == "action":
                player = event.get("player", "")
                action = event.get("action", "")
                if player not in self.state["players"]:
                    raise ValueError("Unknown player")
                if action not in ["attack", "defend", "special"]:
                    raise ValueError("Invalid action")
                current_score = self.state["scores"].get(player, 100)
                if current_score <= 0:
                    raise ValueError("Player is defeated")
                delta = random.choice([-20, 10, 15, 0])
                self.state["scores"][player] = max(0, current_score + delta)
                self.history.append(f"action:{player}:{action}:{delta}")
                return {"status": "action_processed", "score": self.state["scores"][player]}
            elif event_type == "leave":
                player = event.get("player", "")
                if player not in self.state["players"]:
                    raise ValueError("Player not found")
                del self.state["players"][player]
                if player in self.state["scores"]:
                    del self.state["scores"][player]
                self.history.append(f"leave:{player}")
                return {"status": "left", "player": player}
            else:
                raise ValueError(f"Unsupported event type: {event_type}")
        except (ValueError, KeyError) as err:
            self.history.append(f"error:{str(err)}")
            if self.history:
                for item in reversed(self.history[:-1]):
                    if "join:" in item or "action:" in item:
                        break
            return {"status": "error", "message": str(err), "state": self.state.copy()}
        except Exception as err:
            self.history.append(f"critical:{str(err)}")
            for p in list(self.state["scores"].keys()):
                self.state["scores"][p] = max(0, self.state["scores"][p] - 10)
            return {"status": "recovered", "message": "Critical error handled", "state": self.state.copy()}

    def get_current_state(self) -> Dict[str, Any]:
        return self.state.copy()

if __name__ == "__main__":
    gh = GameHandler()
    print(gh.process_event({"type": "join", "player": "Hero"}))
    print(gh.process_event({"type": "action", "player": "Hero", "action": "attack"}))
    print(gh.process_event({"type": "action", "player": "Hero", "action": "invalid"}))
    print(gh.process_event({"type": "join", "player": ""}))
    print(gh.process_event({"type": "leave", "player": "Hero"}))
    print(gh.get_current_state())
