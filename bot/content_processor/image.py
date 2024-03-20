from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import log_photo
from bot.utils.check_permission import CheckUserPermission


class ImageProcessor:

    @classmethod
    def get_user_photo(cls, message: types.Message) -> None:
        """Отвечаем на изобращение."""
        if not CheckUserPermission.check_user(message):
            return log_photo(message)

        bot.send_message(
            message.chat.id,
            text=(
                '''
                У меня нет глаз,
                я не понимаю что на этой картинке.\n'
                Давайте продолжим работать в меню.
                '''
            ),
        )
        return log_photo(message)
