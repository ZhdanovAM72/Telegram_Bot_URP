from telebot import types

from bot import bot
from bot.constants import ADMIN_COMMANDS
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command, logger, log_user_command_updated
from bot.utils.check_permission import CheckUserPermission


class AdminBotCommands:

    @classmethod
    def admin_commands(cls, message: types.Message) -> tuple[types.Message, types.Message] | None:
        """"Направляем список доступных команд администратору."""
        bot.send_message(message.chat.id, 'Проверяем права.')
        if not CheckUserPermission.check_admin(message):
            logger.warning(log_user_command_updated(message))
            return None
        logger.info(log_user_command_updated(message))
        return (bot.send_message(message.chat.id, 'Привет Admin!'),
                bot.send_message(message.chat.id, text=ADMIN_COMMANDS))

    @classmethod
    def create_admin(cls, message: types.Message) -> types.Message | None:
        bot.send_message(message.chat.id, 'Проверяем права.')
        if CheckUserPermission.check_admin(message):
            log_user_command_updated(message)
        else:
            return
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/createmoderator user_code'
        )
        if input_code == '/create_admin':
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
        check = BaseBotSQLMethods.search_email_user(user_id[1].lower().strip())
        if check:
            bot.send_message(message.chat.id, 'Пользователь найден в базе!')
            BaseBotSQLMethods.update_user_to_admin(check, message)
            log_user_command(message)
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')

        log_user_command(message)
        return bot.send_message(
            message.chat.id,
            'Пользователь не найден в системе!\n'
            'Проверьте user_id в БД. '
        )

    @classmethod
    def create_moderator(cls, message: types.Message) -> types.Message | None:
        bot.send_message(message.chat.id, 'Проверяем права.')
        if (CheckUserPermission.check_admin(message)
           or CheckUserPermission.check_moderator(message)):
            log_user_command_updated(message)
        else:
            return
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/createmoderator user_code'
        )
        if input_code == '/create_moderator':
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
        check = BaseBotSQLMethods.search_email_user(user_id[1].lower().strip())
        if check:
            bot.send_message(message.chat.id, 'Пользователь найден в базе!')
            BaseBotSQLMethods.update_user_to_moderator(check, message)
            log_user_command(message)
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')

        log_user_command(message)
        return bot.send_message(
            message.chat.id,
            'Пользователь не найден в системе!\n'
            'Проверьте user_id в БД. '
        )

    @classmethod
    def delete_user_by_email(cls, message: types.Message) -> types.Message | None:
        """Удаляем запись из БД по Email."""
        if (CheckUserPermission.check_admin(message)
           or CheckUserPermission.check_moderator(message)):
            log_user_command_updated(message)
        else:
            return
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/delete_email email'
        )
        delete_user_command = input_code.split()
        if len(delete_user_command) <= 1 or len(delete_user_command) > 2:
            log_user_command(message)
            return bot.send_message(
                message.chat.id,
                erorr_code_message
            )
        logger.debug(delete_user_command[1])
        deleted_email = BaseBotSQLMethods.delete_email(delete_user_command[1].lower().strip())
        logger.debug(deleted_email)
        if deleted_email:
            return bot.send_message(message.chat.id, 'Запись БД удалена!')
        return bot.send_message(
            message.chat.id,
            'Email не найден в системе, либо права пользователя ограничили удаление!\n'
            'Проверьте Email и права пользователя в БД, команда: /dbinfo'
        )

    @classmethod
    def delete_moderator(cls, message: types.Message) -> types.Message | None:
        """Удаляем права модератора из БД по Email."""
        if (CheckUserPermission.check_admin(message)
           or CheckUserPermission.check_moderator(message)):
            log_user_command_updated(message)
        else:
            return
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/delete_moderator email'
        )
        delete_user_command = input_code.split()
        if len(delete_user_command) <= 1 or len(delete_user_command) > 2:
            log_user_command(message)
            return bot.send_message(
                message.chat.id,
                erorr_code_message
            )
        logger.debug(delete_user_command[1])
        deleted_email = BaseBotSQLMethods.delete_moderator_by_email(delete_user_command[1].lower().strip(), message)
        logger.debug(deleted_email)
        if deleted_email:
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')
        return bot.send_message(
            message.chat.id,
            'Email не найден в системе!\n'
            'Проверьте Email в БД. '
        )

    @classmethod
    def delete_admin(cls, message: types.Message) -> types.Message | None:
        """Удаляем права администратора из БД по Email."""
        if CheckUserPermission.check_admin(message):
            log_user_command_updated(message)
        else:
            return
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите запрос как показано на примере!\n'
            'Пример: \n/delete_admin email'
        )
        delete_user_command = input_code.split()
        if len(delete_user_command) <= 1 or len(delete_user_command) > 2:
            log_user_command(message)
            return bot.send_message(
                message.chat.id,
                erorr_code_message
            )
        logger.debug(delete_user_command[1])
        deleted_email = BaseBotSQLMethods.delete_admin_by_email(delete_user_command[1].lower().strip(), message)
        logger.debug(deleted_email)
        if deleted_email:
            return bot.send_message(message.chat.id, 'Запись БД обновлена!')
        return bot.send_message(
            message.chat.id,
            'Email не найден в системе!\n'
            'Проверьте Email в БД. '
        )
