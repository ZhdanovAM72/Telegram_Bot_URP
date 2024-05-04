from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import logger, log_photo
from bot.utils.check_permission import CheckUserPermission

TEXT = "У меня нет глаз, я не понимаю что на этой картинке.\nДавайте продолжим работать в меню."


class ImageProcessor:

    @classmethod
    def get_user_photo(cls, message: types.Message) -> types.Message | None:
        """Отвечаем на изобращение."""
        logger.info(log_photo(message))
        if not CheckUserPermission.check_user(message):
            return None
        return bot.send_message(message.chat.id, text=TEXT)
