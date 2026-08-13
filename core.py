import random
import time

class Game:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.scoreboard = {}

    def add_player(self, player_name):
        if player_name not in self.players:
            self.players.append(player_name)
            self.scoreboard[player_name] = 0

    def update_score(self, player_name, score):
        if player_name in self.scoreboard:
            self.scoreboard[player_name] += score

    def play_round(self):
        round_scores = {player: random.randint(1, 100) for player in self.players}
        for player, score in round_scores.items():
            self.update_score(player, score)
        return round_scores

    def display_scores(self):
        sorted_scores = sorted(self.scoreboard.items(), key=lambda x: x[1], reverse=True)
        for player, score in sorted_scores:
            print(f'{player}: {score}') 

if __name__ == '__main__':
    game = Game('Fun Game')
    game.add_player('Alice')
    game.add_player('Bob')
    for _ in range(5):
        game.play_round()
        game.display_scores()
        time.sleep(1)  
