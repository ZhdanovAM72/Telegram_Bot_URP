from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import log_sticker
from bot.utils.check_permission import CheckUserPermission


class StiсkerProcessor:

    @classmethod
    def get_user_stiсker(cls, message: types.Message) -> None:
        """Ловим отправленные пользователем стикеры."""
        if not CheckUserPermission.check_user(message):
            return log_sticker(message)

        bot.send_message(
            message.chat.id,
            text=(
                '''
                У меня нет глаз, я не вижу этот стикер.
                Давайте продолжим работать в меню.
                '''
            ),
        )
        return log_sticker(message)
