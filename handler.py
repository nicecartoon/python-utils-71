import random
import json


def generate_game_event(player_id, event_type):
    return {
        'player_id': player_id,
        'event_type': event_type,
        'timestamp': random.randint(1, 10000),
    }


def handle_event(event):
    if event['event_type'] == 'score':
        return f"Player {event['player_id']} scored!"
    elif event['event_type'] == 'level_up':
        return f"Player {event['player_id']} leveled up!"
    else:
        return f"Unhandled event type: {event['event_type']}"


def process_events(events):
    results = []
    for event in events:
        result = handle_event(event)
        results.append(result)
    return results


def main():
    players = [1, 2, 3]
    events = [generate_game_event(random.choice(players), random.choice(['score', 'level_up'])) for _ in range(5)]
    results = process_events(events)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()