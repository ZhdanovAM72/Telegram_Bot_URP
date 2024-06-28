from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class ChangeEmploymentContract:

    @staticmethod
    def change_employment_contract(message: types.Message) -> types.Message:
        buttons = [
            "Переводы",
            "Дополнительная работа",
            "Режим рабочего времени",
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            "Изменение трудового договора",
            reply_markup=markup,
        )
