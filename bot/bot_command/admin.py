from telebot import types

from bot import bot
from bot.constants import ADMIN_COMMANDS
from bot.db import BaseBotSQLMethods
from bot.utils.code_generator import CodeGenerator
from bot.logger_setting.logger_bot import log_user_command
from bot.utils.check_permission import CheckUserPermission


class AdminBotCommands:

    @classmethod
    def admin_commands(cls, message: types.Message) -> None:
        """"Направляем список доступных команд администратору."""
        bot.send_message(message.chat.id, 'Проверяем права.')
        if not CheckUserPermission.check_admin(message):
            log_user_command(message)
            return None
        bot.send_message(message.chat.id, 'Привет Admin!')
        bot.send_message(message.chat.id, text=ADMIN_COMMANDS)
        return log_user_command(message)

    @classmethod
    def update_code(cls, message: types.Message) -> None:
        """Обновляем код пользователя в БД."""
        if not CheckUserPermission.check_admin(message):
            log_user_command(message)
            return None
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/updatecode old_code es'
        )
        if input_code == '/updatecode':
            bot.send_message(
                message.chat.id,
                erorr_code_message
            )
            return log_user_command(message)
        old_code = input_code.split()
        if len(old_code) <= 2 or len(old_code) > 3:
            return bot.send_message(
                message.chat.id,
                erorr_code_message
            )
        check = BaseBotSQLMethods.search_code_in_db(old_code[1])
        if check is not None and check[0] == str(old_code[1]):
            company_name = old_code[2]
            new_code = CodeGenerator.generate_code(company_name.lower())
            BaseBotSQLMethods.update_user_code(old_code[1], new_code)
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')
        bot.send_message(
            message.chat.id,
            'Код не найден в системе!\n'
            'Проверьте code в БД. '
        )
        return log_user_command(message)

    @classmethod
    def create_moderator(message: types.Message) -> None:
        """Создаем модератора."""
        bot.send_message(message.chat.id, 'Проверяем права.')
        if not CheckUserPermission.check_admin(message):
            log_user_command(message)
            return None
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/createmoderator user_code'
        )
        if input_code == '/createmoderator':
            bot.send_message(
                message.chat.id,
                erorr_code_message
            )
            return log_user_command(message)
        user_id = input_code.split()
        if len(user_id) <= 1 or len(user_id) > 2:
            return bot.send_message(
                message.chat.id,
                erorr_code_message
            )
        check = BaseBotSQLMethods.search_user_id_in_db(user_id[1])
        if check is not None and check[0] == int(user_id[1]):
            bot.send_message(message.chat.id, 'Пользователь найден в базе!')
            moderator_code = 'moderator-' + check[1]
            BaseBotSQLMethods.update_user_to_moderator(
                moderator_code, user_id[1]
            )
            log_user_command(message)
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')
        bot.send_message(
            message.chat.id,
            'Пользователь не найден в системе!\n'
            'Проверьте user_id в БД. '
        )
        return log_user_command(message)

    @classmethod
    def delete_user_from_db(cls, message: types.Message) -> None:
        """Удаляем запись из БД по user_id."""
        if not CheckUserPermission.check_admin(message):
            return log_user_command(message)
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/deleteuser user_id\n/deletecode user_code'
        )
        delete_user_command = input_code.split()
        if len(delete_user_command) <= 1 or len(delete_user_command) > 2:
            bot.send_message(
                message.chat.id,
                erorr_code_message
            )
            return log_user_command(message)

        if delete_user_command[0] == '/deleteuser':
            cls.__delete_user_by_id(message, delete_user_command[1])
            return None

        elif delete_user_command[0] == '/deletecode':
            cls.__delete_user_by_code(message, delete_user_command[1])
            return None

        return None

    @staticmethod
    def __delete_user_by_id(message: types.Message, user_id: str):
        check = BaseBotSQLMethods.search_user_id_in_db(user_id)
        if check is not None and check[0] == int(user_id):
            bot.send_message(message.chat.id, 'Код найден в базе!')
            BaseBotSQLMethods.delete_by_chat_id(user_id)
            bot.send_message(message.chat.id, 'Запись БД удалена!')
            return log_user_command(message)
        bot.send_message(
            message.chat.id,
            'Пользователь не найден в системе!\n'
            'Проверьте user_id в БД. '
        )
        return log_user_command(message)

    @staticmethod
    def __delete_user_by_code(message: types.Message, user_code: str):
        check = BaseBotSQLMethods.search_code_in_db(user_code)
        if check is not None and check[0] == user_code:
            bot.send_message(message.chat.id, 'Код найден в базе!')
            BaseBotSQLMethods.delete_by_code(user_code)
            return bot.send_message(message.chat.id, 'Запись БД удалена!')
        bot.send_message(
            message.chat.id,
            'Код не найден в системе!\n'
            'Проверьте код в БД. '
        )
        return log_user_command(message)
