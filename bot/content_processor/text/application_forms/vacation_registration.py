from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class VacationRegistration:

    @staticmethod
    def vacation_registration_main(message: types.Message) -> types.Message:
        buttons = [
            'Другие виды отпусков',
            'Отмена, отзыв из отпуска',
            'Отпуск без сохранения зп',
            'Перенос, продление отпуска',
            'Сдача крови',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            "Оформление отпусков",
            reply_markup=markup,
        )
