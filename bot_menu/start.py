import telebot
from telebot import types

from db import BaseBotSQLMethods
from constant import NOT_REGISTERED
from logger_setting.logger_bot import log_user_command


class StartBotCommand:

    @classmethod
    def check_user_permissions(cls, message: telebot.types.Message):
        from main import bot
        """"Определяем права пользователя."""
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
            cls.start(message)
        else:
            bot.send_message(message.chat.id, 'Непредвиденная ошибка.')

    @classmethod
    def start(cls, message: telebot.types.Message):
        from main import bot
        """Приветствуем пользователя и включаем меню бота."""
        check_user = BaseBotSQLMethods.get_user_access(message.chat.id)
        if check_user is None or check_user[1] != message.chat.id:
            return bot.send_message(message.chat.id, NOT_REGISTERED)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton('Информация о боте')
        button_2 = types.KeyboardButton('Главное меню')
        markup.add(button_1, button_2)

        if (message.from_user.first_name is not None and
           message.from_user.last_name is not None):
            user_info = (
                f'{message.from_user.first_name} '
                f'{message.from_user.last_name}'
            )

        elif (message.from_user.first_name is not None and
              message.from_user.last_name is None):
            user_info = f'{message.from_user.username}'

        elif (message.from_user.username is None and
              message.from_user.last_name is None):
            user_info = f'{message.from_user.first_name}'

        else:
            user_info = 'сотрудник'

        start_message = (f'Здравствуйте, <b>{user_info}</b>!\n'
                         'Я расскажу Вам о нефтесервисных активах! '
                         'выберите интересующую Вас тему в меню.')
        bot.send_message(
            message.chat.id,
            start_message, parse_mode='html',
            reply_markup=markup,
        )
        return log_user_command(message)