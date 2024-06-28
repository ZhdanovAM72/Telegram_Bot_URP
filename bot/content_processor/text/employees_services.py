from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class EmployeesServices:

    def services_for_employees(message: types.Message) -> types.Message:
        buttons = [
            'Сервисы самообслуживания',
            'Контакт центр',
            '🔙 вернуться в раздел О компании',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            text="⬇ Сервисы для сотрудников",
            reply_markup=markup,
        )

    def self_services(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/сервисы_для_сотрудников/'
                    'портал_самообслуживания/техническая_поддержка.pdf']
        caption = ['Сервисы самообслуживания']
        Documents.send_document_with_markup(message.chat.id, document, caption)

    def contact_center(message: types.Message) -> types.Message:
        document = ['prod_data/о_компании/сервисы_для_сотрудников/'
                    'контакт_центр/ОЦО.pdf']
        caption = ['Контакт центр ОЦО']
        Documents.send_document_with_markup(message.chat.id, document, caption)
