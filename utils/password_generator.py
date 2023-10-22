from random import choice

PASS_RANGE = 16
EASY_PASS_RANGE = 4

# Базовый генератор кодов (сложные значения)
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
    """Генератор уникального кода доступа по ДО."""
    if company == 'es':  # Энергосистемы
        code = easy_code()
        return company + code
    if company == 'st':  # Сервисные технологии
        code = easy_code()
        return company + code
    if company == 'nr':  # Нефтесервисные решения
        code = easy_code()
        return company + code
    if company == 'its':  # Инженерно-технологический сервис
        code = easy_code()
        return company + code
    return False


# Упрощенный генератор
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
