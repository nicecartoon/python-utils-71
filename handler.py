import random
import json

class GameHandler:
    def __init__(self):
        self.players = []
        self.scoreboard = {}

    def add_player(self, player_name):
        if player_name not in self.players:
            self.players.append(player_name)
            self.scoreboard[player_name] = 0
        else:
            raise ValueError(f'Player {player_name} already exists.')

    def update_score(self, player_name, points):
        if player_name in self.players:
            self.scoreboard[player_name] += points
        else:
            raise ValueError(f'Player {player_name} not found.')

    def get_winner(self):
        if not self.players:
            raise ValueError('No players to determine a winner.')
        return max(self.scoreboard, key=self.scoreboard.get)

    def save_game_state(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.scoreboard, f)

    def load_game_state(self, filename):
        with open(filename, 'r') as f:
            self.scoreboard = json.load(f)
            self.players = list(self.scoreboard.keys())

    def random_event(self):
        event_outcome = random.choice(['bonus', 'penalty'])
        return event_outcome