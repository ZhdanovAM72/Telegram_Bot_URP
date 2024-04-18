from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class ApplicationForms:

    @staticmethod
    def application_forms_main(message: types.Message) -> types.Message:
        buttons = [
            'Авансовый отчет',
            'Банковские реквизиты',
            'Изменение трудового договора',
            'Оформление отпусков',
            'Прекращение трудового договора',
            'Рождение ребенка',
            'Учет рабочего времени',
            '🔙 Главное меню',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            'Бланки заявлений',
            reply_markup=markup,
        )
