import json
import hashlib
from collections import defaultdict
from typing import List, Dict, Any

def process_gaming_data(raw_data: str) -> Dict[str, Any]:
    data = json.loads(raw_data)
    session_scores = defaultdict(list)
    for item in data:
        if isinstance(item, dict) and 'session_id' in item and 'score' in item:
            session_id = item['session_id']
            score = item.get('score', 0)
            hashed = hashlib.md5(session_id.encode()).hexdigest()[:8]
            session_scores[hashed].append(score)
    aggregated = {}
    for h, scores in session_scores.items():
        if scores:
            aggregated[h] = {
                'count': len(scores),
                'total': sum(scores),
                'max': max(scores),
                'avg': sum(scores) / len(scores)
            }
    return aggregated

def filter_valid_game_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    valid_events = [
        event for event in events
        if isinstance(event, dict) and 'type' in event and 'value' in event and event['value'] > 0
    ]
    return valid_events

def compute_leaderboard(players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sorted_players = sorted(
        players,
        key=lambda p: (-p.get('score', 0), p.get('name', ''))
    )
    leaderboard = []
    for rank, player in enumerate(sorted_players, 1):
        player_copy = player.copy()
        player_copy['rank'] = rank
        leaderboard.append(player_copy)
    return leaderboard

def flatten_game_inventory(inventory: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
    items = {}
    for k, v in inventory.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_game_inventory(v, new_key))
        elif isinstance(v, list):
            for idx, item in enumerate(v):
                if isinstance(item, dict):
                    items.update(flatten_game_inventory(item, f"{new_key}[{idx}]"))
                else:
                    items[f"{new_key}[{idx}]"] = item
        else:
            items[new_key] = v
    return items