from telebot import types

from bot import bot
from bot.utils.buttons import Buttons
from bot.db import BaseBotSQLMethods


START_MESSAGE = (
    'Здравствуйте, <b>{0}</b>!\n'
    'Я расскажу Вам о нефтесервисных активах! '
    'выберите интересующую Вас тему в меню.'
)


class StartBotCommand:

    @classmethod
    def start_command(cls, message: types.Message) -> None:
        user_db = BaseBotSQLMethods.search_telegram_id_user(message.chat.id)
        if user_db == message.chat.id:
            return bot.send_message(message.chat.id, 'Вы уже зарегистрированы!')
        markup = Buttons.create_inline_keyboard(buttons=(('Зарегистрироваться', 'start_register'),), callback=True)
        return bot.send_message(message.chat.id, 'Здравствуйте! Пожалуйста, зарегистрируйтесь.', reply_markup=markup)
