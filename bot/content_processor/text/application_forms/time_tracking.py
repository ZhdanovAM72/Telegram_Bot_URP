from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class TimeTracking:

    @staticmethod
    def time_tracking(message: types.Message) -> types.Message:
        buttons = [
            'Изменение графика работы',
            'Исполнение гос.обязанностей',
            'Простой, задержка в пути',
            'Работа в выходной день',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.chat.id,
            'Учет рабочего времени',
            reply_markup=markup,
        )
