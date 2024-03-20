import os

import telebot

from bot import bot
from bot.logger_setting.logger_bot import log_user_command
from bot.utils.check_permission import CheckUserPermission


class StopBotCommand:

    @classmethod
    def stop_command(cls, message: telebot.types.Message) -> None:
        """Останавливаем работу бота командой."""
        if not CheckUserPermission.check_admin(message):
            return None
        bot.send_message(message.chat.id, 'OK, stop...')
        log_user_command(message)
        return bot.stop_polling()
