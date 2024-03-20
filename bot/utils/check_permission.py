import telebot

from bot.db import BaseBotSQLMethods
from bot.constant import NOT_REGISTERED, NO_ADMIN_RIGHTS
from bot import bot


class CheckUserPermission:

    @classmethod
    def check_user(cls, message: telebot.types.Message) -> bool:
        """"Проверяем права пользователя."""
        access = BaseBotSQLMethods.get_user_access(message.chat.id)
        if access is None:
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
        elif access[1] == message.chat.id:
            return True
        else:
            bot.send_message(message.chat.id, 'Непредвиденная ошибка.')
            return False

    @classmethod
    def check_admin(cls, message: telebot.types.Message) -> bool:
        """Проверяем является ли пользователь администратором."""
        access = BaseBotSQLMethods.get_admin_access(message.chat.id)
        if access is None or access[1] != message.chat.id:
            bot.send_message(message.chat.id, text=NO_ADMIN_RIGHTS)
            return False
        return True
