from telebot import types
from bot.utils.buttons import Buttons
from bot import bot

INFO_MESSAGE = (
    'Переходи в главное меню и узнай самую важную '
    'информацию о нефтесервисных активах!\n'
    '\nДля администратора и модераторов чат-бота '
    'доступны дополнительные команды:\n'
    '/admin\n'
    '/moderator\n'
)


class BotInformation:

    @staticmethod
    def bot_information(message: types.Message) -> types.Message:
        message.text == "Неизвестная команда"
        buttons = (
            "Главное меню",
        )
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.from_user.id,
            text=INFO_MESSAGE,
            reply_markup=markup,
        )
