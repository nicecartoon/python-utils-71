class GameError(Exception):
    pass

class InvalidMoveError(GameError):
    def __init__(self, move):
        super().__init__(f'Invalid move: {move}')
        self.move = move

class OutOfBoundsError(GameError):
    def __init__(self, position):
        super().__init__(f'Position out of bounds: {position}')
        self.position = position

class LevelNotFoundError(GameError):
    def __init__(self, level_id):
        super().__init__(f'Level not found: {level_id}')
        self.level_id = level_id

class InsufficientResourcesError(GameError):
    def __init__(self, resource):
        super().__init__(f'Insufficient resources: {resource}')
        self.resource = resource

class GameNotStartedError(GameError):
    def __init__(self, game_id):
        super().__init__(f'Game not started: {game_id}')
        self.game_id = game_id

class PlayerNotFoundError(GameError):
    def __init__(self, player_id):
        super().__init__(f'Player not found: {player_id}')
        self.player_id = player_id