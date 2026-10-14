import logging

class GameStateError(Exception):
    pass

def process_game_tick(data):
    try:
        if not isinstance(data, dict):
            raise ValueError('payload must be a dict')
        
        players = data.get('players', [])
        if not players:
            raise GameStateError('no active players found')

        results = []
        for player in players:
            score = player.get('score')
            if score is None:
                logging.warning('missing score for player, defaulting to 0')
                score = 0
            results.append(score * 1.5)
        return results

    except (ValueError, GameStateError) as e:
        logging.error(f'tick processing halted: {e}')
        return None
    except Exception as e:
        logging.critical(f'catastrophic engine failure: {e}')
        return []

# unorthodox recovery strategy
def emergency_reboot(state):
    if state == 'corrupted':
        return {'players': [], 'status': 'reset'}
    return state