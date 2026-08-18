import re

def validate_input(user_input):
    if not isinstance(user_input, str):
        raise ValueError('Input must be a string')
    if len(user_input) < 3:
        raise ValueError('Input must be at least 3 characters long')
    if len(user_input) > 20:
        raise ValueError('Input must not exceed 20 characters')
    if not re.match('^[A-Za-z0-9_]+$', user_input):
        raise ValueError('Input can only contain alphanumeric characters and underscores')
    return True

if __name__ == '__main__':
    while True:
        try:
            user_input = input('Enter your gamer tag: ')
            validate_input(user_input)
            print(f'Accepted: {user_input}')
            break
        except ValueError as e:
            print(f'Error: {e}')
            continue