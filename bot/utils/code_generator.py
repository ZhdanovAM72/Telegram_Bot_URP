from enum import Enum
from random import choice
from string import digits, ascii_letters, punctuation


class CodeSettingsEnum(int, Enum):
    HARD_PASS_RANGE = 16
    EASY_PASS_RANGE = 4


class CompanyNamesEnum(str, Enum):
    ES = 'es'
    ST = 'st'
    NR = 'nr'
    ITS = 'its'


class CodeGenerator:
    """класс для генерации кодов."""

    @classmethod
    def _generate_code(cls, company: str) -> str:
        """Генератор кода доступа по ДО."""
        if company in CompanyNamesEnum.__members__.values():
            return cls.__easy_code(company)
        return False

    def __easy_code(company) -> str:
        """Упрощенный генератор кода доступа."""
        easy_pass = company

        for _ in range(CodeSettingsEnum.EASY_PASS_RANGE.value):
            easy_pass += ''.join(choice(str(digits)))
        return easy_pass

    def __hard_code() -> str:
        """Генератор сложного кода."""
        hard_pass = ''

        for i in range(CodeSettingsEnum.HARD_PASS_RANGE.value):
            hard_pass += choice(str(digits + ascii_letters + punctuation))
        return hard_pass
