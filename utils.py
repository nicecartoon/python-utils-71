import random

class Game:
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0

    def play_round(self, player_choice):
        valid_choices = ['rock', 'paper', 'scissors']
        if player_choice not in valid_choices:
            raise ValueError('Invalid choice! Choose rock, paper, or scissors.')

        computer_choice = random.choice(valid_choices)
        print(f'Computer chose: {computer_choice}')

        if (player_choice == computer_choice):
            return 'Draw'
        elif (player_choice == 'rock' and computer_choice == 'scissors') or  \
             (player_choice == 'paper' and computer_choice == 'rock') or  \
             (player_choice == 'scissors' and computer_choice == 'paper'):
            self.player_score += 1
            return 'Player wins'
        else:
            self.computer_score += 1
            return 'Computer wins'

    def get_scores(self):
        return {'Player Score': self.player_score, 'Computer Score': self.computer_score}

if __name__ == '__main__':
    game = Game()
    while True:
        user_input = input('Enter rock, paper, or scissors (or type exit): ').lower()
        if user_input == 'exit':
            print('Thanks for playing!')
            break
        try:
            result = game.play_round(user_input)
            print(result)
            print(game.get_scores())
        except ValueError as e:
            print(e)