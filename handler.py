import random

class GameHandler:
    def __init__(self, players):
        self.players = players
        self.current_round = 0

    def start_game(self):
        print(f"Starting game with {len(self.players)} players...")
        self.play_rounds()

    def play_rounds(self):
        while self.current_round < 5:
            self.current_round += 1
            self.play_round()

    def play_round(self):
        print(f"Round {self.current_round}")
        for player in self.players:
            score = self.roll_dice()
            print(f"{player} rolled a {score}")

    def roll_dice(self):
        return random.randint(1, 6)

if __name__ == '__main__':
    players = ["Alice", "Bob", "Charlie"]
    game = GameHandler(players)
    game.start_game()