from telebot import types

from bot import bot
from bot.constants import MODERATOR_COMMANDS
# from bot.db import BaseBotSQLMethods
# from bot.utils.code_generator import CodeGenerator
from bot.logger_setting.logger_bot import log_user_command
from bot.utils.check_permission import CheckUserPermission


class ModeratorBotCommands:

    @classmethod
    def moderator_commands(cls, message: types.Message) -> None:
        """"Направляем список команд доступных модератору."""
        bot.send_message(message.chat.id, 'Проверяем права.')
        if not CheckUserPermission.check_moderator(message):
            log_user_command(message)
            return None
        bot.send_message(message.chat.id, 'Привет Moderator!')
        bot.send_message(message.chat.id, text=MODERATOR_COMMANDS)
        return log_user_command(message)
