from enum import Enum
from random import choice


class CodeSettingsEnum(int, Enum):
    PASS_RANGE = 16
    EASY_PASS_RANGE = 4


class CodeGenerator:
    """класс для генерации кодов."""

    @classmethod
    def _generate_code(cls, company) -> str:
        """Генератор уникального кода доступа по ДО."""
        if company == 'es':  # Энергосистемы
            code = cls.__easy_code()
            return company + code
        if company == 'st':  # Сервисные технологии
            code = cls.__easy_code()
            return company + code
        if company == 'nr':  # Нефтесервисные решения
            code = cls.__easy_code()
            return company + code
        if company == 'its':  # Инженерно-технологический сервис
            code = cls.__easy_code()
            return company + code
        return False

    @classmethod
    def __easy_code(cls) -> str:
        """Упрощенный генератор уникального кода доступа."""
        digits: str = '0123456789'
        ally: str = digits

        chars = ''
        chars += ally
        easy_pass = ''

        for i in range(CodeSettingsEnum.EASY_PASS_RANGE.value):
            easy_pass += choice(chars)
        return easy_pass
