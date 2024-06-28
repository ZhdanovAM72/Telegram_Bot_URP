from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class Feedback:

    @staticmethod
    def feedback(message: types.Message) -> types.Message:
        buttons = [
            ["Заполнить форму", "https://forms.yandex.ru/u/64f4d1a4068ff09dca58ac3c/"],
        ]
        markup = Buttons.create_inline_keyboard(buttons=buttons)
        return bot.send_message(
            message.chat.id,
            'Форма обратной связи',
            reply_markup=markup
        )
