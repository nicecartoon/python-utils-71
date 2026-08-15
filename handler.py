import json
from typing import Dict, Any

class GameDataHandler:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def get_player_score(self, player_id: str) -> int:
        player_data = self.data.get(player_id, {})
        return player_data.get('score', 0)

    def update_player_score(self, player_id: str, score: int) -> None:
        if player_id in self.data:
            self.data[player_id]['score'] = score
        else:
            self.data[player_id] = {'score': score}

    def save_data_to_file(self, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    @staticmethod
    def load_data_from_file(filename: str) -> Dict[str, Any]:
        with open(filename, 'r') as file:
            return json.load(file)

# Example usage:
if __name__ == '__main__':
    game_data = GameDataHandler.load_data_from_file('game_data.json')
    handler = GameDataHandler(game_data)
    handler.update_player_score('player1', 50)
    handler.save_data_to_file('updated_game_data.json')