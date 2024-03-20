from telebot import types

from bot import bot
from bot.constant import ADMIN_COMMANDS
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
