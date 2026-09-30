import time

class GameInputValidator:
    def __init__(self, bounds=(0, 1000)):
        self.bounds = bounds

    def __call__(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError(f'Invalid input type: {type(val)}')
        if not (self.bounds[0] <= val <= self.bounds[1]):
            raise ValueError(f'Input {val} out of bounds {self.bounds}')
        return val

def main_loop():
    validator = GameInputValidator()
    queue = [10, 'trash', 500, 1500, 42]
    
    while queue:
        data = queue.pop(0)
        try:
            validated = validator(data)
            print(f'Processing valid input: {validated}')
        except ValueError as e:
            print(f'Input rejection: {e}')
        finally:
            time.sleep(0.1)

if __name__ == '__main__':
    main_loop()