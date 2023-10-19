from random import choice

PASS_RANGE = 16
EASY_PASS_RANGE = 4


# def generate_code() -> str:
#     """Генератор уникального кода доступа."""
#     digits: str = '0123456789'
#     uppercase: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     lowercase: str = 'abcdefghijklmnopqrstuvwxyz'
#     punctuation: str = '!#$%&*+-=?@^_'
#     ally: str = digits + uppercase + lowercase + punctuation

#     chars = ''
#     chars += ally
#     password = ''

#     for i in range(PASS_RANGE):
#         password += choice(chars)
#     return password


def generate_code(company) -> str:
    """Генератор уникального кода доступа."""
    if company == 'es':
        code = easy_code()
        return company + code
    if company == 'st':
        code = easy_code()
        return company + code
    if company == 'nr':
        code = easy_code()
        return company + code
    if company == 'its':
        code = easy_code()
        return company + code
    return False


def easy_code() -> str:
    """Генератор уникального кода доступа."""
    digits: str = '0123456789'
    ally: str = digits

    chars = ''
    chars += ally
    easy_pass = ''

    for i in range(EASY_PASS_RANGE):
        easy_pass += choice(chars)
    return easy_pass
