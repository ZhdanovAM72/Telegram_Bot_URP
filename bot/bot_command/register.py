from telebot import types

from bot import bot
from bot.bot_command.start import StartBotCommand
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import logger


class RegisterUserCommand:

    @classmethod
    def register(cls, call: types.CallbackQuery) -> types.Message:
        bot.send_message(call.message.chat.id, 'Введите логин (логин от учетной записи до символа "@"):')
        return bot.register_next_step_handler(call.message, cls.login_input)

    @classmethod
    def login_input(cls, message: types.Message) -> None:
        login = message.text.lower()
        if not BaseBotSQLMethods.search_email_in_db(login):
            return bot.send_message(message.chat.id, 'Ошибка поиска логина, загеристрируйтесь повторно!')
        bot.send_message(message.chat.id, 'Введите свой табельный номер:')
        return bot.register_next_step_handler(message, lambda msg: cls.password_input(msg, login))

    @classmethod
    def password_input(cls, message: types.Message, login: str) -> None:
        try:
            password = int(message.text)
        except ValueError:
            logger.error('Error tab_number')
            return bot.send_message(
                message.chat.id,
                'Вы не зарегистрированы! Ошибочный табельный номер! \n'
                'Используйте цифры (максимальное значение 1 млн.)!',
            )
        else:
            if password > 1_000_000 or password < 1:
                return bot.send_message(
                    message.chat.id,
                    'Вы не зарегистрированы! Ошибочный табельный номер! \n'
                    'Используйте цифры (максимальное значение 1 млн.)!',
                )

            if not BaseBotSQLMethods.search_tab_number_in_db(password):
                return bot.send_message(message.chat.id, 'Вы не зарегистрированы! Данный табельный номер занят!')

            if not BaseBotSQLMethods.search_telegram_id_in_db(message.chat.id):
                return bot.send_message(message.chat.id, 'Вы не зарегистрированы! Данный id занят!')

            BaseBotSQLMethods.user_sign_up(email=login, tab_number=password, message=message)

            full_name = BaseBotSQLMethods.search_full_name_in_db(message.chat.id)
            if full_name:
                return bot.send_message(message.chat.id, f'{full_name} - Вы зарегистрированы!')
        return bot.send_message(message.chat.id, 'Ошибка поиска данных...')
