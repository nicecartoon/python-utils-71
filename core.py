import time
import random

class Game:
    def __init__(self, name):
        self.name = name
        self.level = 0
        self.score = 0

    def play(self):
        self.level += 1
        score_increment = self.calculate_score()
        self.score += score_increment
        return score_increment

    def calculate_score(self):
        return random.randint(1, 100) * self.level

    def simulate_gameplay(self, rounds):
        results = []
        start_time = time.time()
        for _ in range(rounds):
            score = self.play()
            results.append(score)
        total_time = time.time() - start_time
        avg_score = sum(results) / len(results)
        return avg_score, total_time

if __name__ == '__main__':
    game = Game('Warrior Quest')
    average_score, elapsed_time = game.simulate_gameplay(1000)
    print(f'Average Score: {average_score}, Time Taken: {elapsed_time} seconds')