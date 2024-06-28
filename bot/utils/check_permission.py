import telebot

from bot.db import BaseBotSQLMethods
from bot.constants import NOT_REGISTERED, NO_ADMIN_RIGHTS, NO_MODERATOR_RIGHTS
from bot import bot


class CheckUserPermission:

    @classmethod
    def check_user(cls, message: telebot.types.Message) -> bool:
        """"Проверяем права пользователя."""
        access = BaseBotSQLMethods.get_user_access(message.chat.id)
        if not access:
            bot.send_message(message.chat.id, NOT_REGISTERED)
            bot.send_message(
                message.chat.id,
                'Запросите код у администратора проекта, '
                'либо используйте имеющийся.'
            )
            bot.send_message(
                message.chat.id,
                'Чтобы зарегистрироваться введите актуальный код доступа'
                ' через пробел после команды "/code"'
            )
            bot.send_message(
                message.chat.id,
                'пример кода:\n/code es1nngg2f^st3!nr4\n'
                '(Внимание код одноразовый!)'
            )
        elif access:
            return True
        else:
            bot.send_message(message.chat.id, 'Непредвиденная ошибка.')
            return False

    @classmethod
    def check_admin(cls, message: telebot.types.Message) -> bool:
        """Проверяем является ли пользователь администратором."""
        access = BaseBotSQLMethods.get_admin_access(message.chat.id)
        if not access:
            bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
            return False
        return True

    @classmethod
    def check_moderator(cls, message: telebot.types.Message) -> bool:
        """Проверяем является ли пользователь модератором."""
        access = BaseBotSQLMethods.get_moderator_access(message.chat.id)
        if not access:
            bot.send_message(message.chat.id, text=NO_MODERATOR_RIGHTS)
            return False
        return True
