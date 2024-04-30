import telebot
from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import log_user_command
from bot.utils.check_permission import CheckUserPermission


class StartBotCommand:

    @staticmethod
    def start(message: telebot.types.Message):
        """Приветствуем пользователя и включаем меню бота."""
        if not CheckUserPermission.check_user(message):
            return None
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1 = types.KeyboardButton('Информация о боте')
        button_2 = types.KeyboardButton('Главное меню')
        markup.add(button_1, button_2)

        if (message.from_user.first_name is not None and
           message.from_user.last_name is not None):
            user_info = (
                f'{message.from_user.first_name} {message.from_user.last_name}'
            )

        elif (message.from_user.first_name is not None and
              message.from_user.last_name is None):
            user_info = message.from_user.first_name

        elif message.from_user.username is not None:
            user_info = message.from_user.username

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
