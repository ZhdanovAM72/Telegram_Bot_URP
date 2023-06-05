from random import choice

PASS_RANGE = 16


def generate_code() -> str:
    digits: str = '0123456789'
    uppercase: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase: str = 'abcdefghijklmnopqrstuvwxyz'
    punctuation: str = '!#$%&*+-=?@^_'
    ally: str = digits + uppercase + lowercase + punctuation

    chars = ''
    chars += ally
    password = ''

    for i in range(PASS_RANGE):
        password += choice(chars)
    print(password)
    return password
