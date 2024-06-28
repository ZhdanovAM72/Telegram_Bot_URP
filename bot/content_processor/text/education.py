from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot


class Education:

    @staticmethod
    def education(message: types.Message) -> types.Message:
        buttons = [
            'Цикл планирования обучения',
            'Каталог программ',
            'Полезная литература',
            'Планирование обучения',
            '🔙 вернуться в раздел Цикл управления талантами',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text="⬇ Обучение",
            reply_markup=markup,
        )

    @staticmethod
    def planning_education(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Обучение/ГПН_ЭС/plan/'
        documents = (
            {
                'file': open(f'{parrent_path}employee.pdf', 'rb'),
                'caption': 'Планирование обучения - Сотрудник',
            },
            {
                'file': open(f'{parrent_path}supervisor.pdf', 'rb'),
                'caption': 'Планирование обучения - Руководитель',
            },
        )
        Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    def useful_literature(message: types.Message) -> types.Message:
        document = ('prod_data/Обучение/ГПН_ЭС/Почитать/электронные_библиотеки.pdf',)
        caption = ('Электронные библиотеки',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def training_planning_cycle(message: types.Message) -> types.Message:
        document = ('prod_data/Обучение/ГПН_ЭС/Целевые_образовательные_программы/educate.pdf',)
        caption = ('Цикл планирования обучения',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def program_catalog(message: types.Message) -> types.Message:
        document = ('prod_data/Обучение/ГПН_ЭС/Каталог_программ/Рекомендованные_образовательные_программы.pdf',)
        caption = ('Рекомендованные образовательные программы',)
        Documents.send_document_with_markup(message.chat.id, document, caption)
