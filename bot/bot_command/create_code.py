from telebot import types

from bot import bot
from bot.db import BaseBotSQLMethods
from bot.utils.check_permission import CheckUserPermission
from bot.utils.code_generator import CodeGenerator
from bot.logger_setting.logger_bot import log_user_command


class CreateCodeCommands:

    @classmethod
    def create_code(cls, message: types.Message) -> None:
        """Создание кода доступа."""
        if (CheckUserPermission.check_admin(message) or
           CheckUserPermission.check_moderator(message)):
            log_user_command(message)
        else:
            return None

        company = message.text.split('_')
        company_name = company[1]
        generate__new_code = CodeGenerator._generate_code(company_name.lower())
        check = BaseBotSQLMethods.search_code_in_db(generate__new_code)
        if check is not None and check[0] == generate__new_code:
            bot.send_message(
                message.chat.id,
                'Данный код уже существует, '
                'повторите команду.'
            )
        elif check is None:
            BaseBotSQLMethods.create_new_code(generate__new_code)
            bot.send_message(message.chat.id,
                             'Код сохранен и доступен для регистрации:')
            bot.send_message(message.chat.id, f'/code {generate__new_code}')
        else:
            bot.send_message(message.chat.id, 'Непредвиденная ошибка.')

        return log_user_command(message)
