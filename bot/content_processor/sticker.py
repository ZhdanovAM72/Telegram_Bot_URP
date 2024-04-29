from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import logger, log_sticker
from bot.utils.check_permission import CheckUserPermission

TEXT = "У меня нет глаз, я не вижу этот стикер. Давайте продолжим работать в меню."


class StiсkerProcessor:

    @staticmethod
    def get_user_stiсker(message: types.Message) -> None | types.Message:
        """Ловим отправленные пользователем стикеры."""
        if not CheckUserPermission.check_user(message):
            return logger.info(log_sticker(message))
        logger.info(log_sticker(message))
        return bot.send_message(message.chat.id, text=TEXT)
