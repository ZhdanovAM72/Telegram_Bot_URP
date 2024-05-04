from telebot import types

from bot import bot
from bot.constants import MODERATOR_COMMANDS
from bot.logger_setting.logger_bot import logger, log_user_command_updated
from bot.utils.check_permission import CheckUserPermission


class ModeratorBotCommands:

    @classmethod
    def moderator_commands(cls, message: types.Message) -> types.Message | None:
        """"Направляем список команд доступных модератору."""
        bot.send_message(message.chat.id, 'Проверяем права.')
        if not CheckUserPermission.check_moderator(message):
            logger.warning(log_user_command_updated(message))
            return None

        logger.info(log_user_command_updated(message))
        return (bot.send_message(message.chat.id, 'Привет Moderator!'),
                bot.send_message(message.chat.id, text=MODERATOR_COMMANDS))
