from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ABOUT_NTK


class YouthPolicy:

    @staticmethod
    def youth_policy(message: types.Message) -> types.Message:
        buttons = [
            'Молодежный совет',
            'Организация практики',
            'Развитие молодых специалистов',
            '🔙 Главное меню',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Молодежная политика",
            reply_markup=markup,
        )

    @staticmethod
    def organization_of_practice(message: types.Message) -> types.Message:
        document = ('prod_data/Молодежная_политика/org_practics/practis.pdf',)
        caption = ('Прохождение практики в Компании',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def youth_council(message: types.Message) -> types.Message:
        buttons = [
            'Направления деятельности МС',
            'Положение, мотивация МС',
            'Структура МС',
            '🔙 вернуться в раздел Молодежная политика',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Молодежный совет",
            reply_markup=markup,
        )

    @staticmethod
    def youth_council_activity(message: types.Message) -> types.Message:
        document = ('prod_data/Молодежная_политика/MS/Направления_деятельности/napravlenya.pdf',)
        caption = ('Направления деятельности МС',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def youth_council_documents(message: types.Message) -> types.Message:
        parrent_path = 'prod_data/Молодежная_политика/MS/Положение_мотивация/'
        documents = (
            f'{parrent_path}workorgMS.pdf',
            f'{parrent_path}trackMS.pdf',
            f'{parrent_path}AnketaMS.docx',
        )
        captions = (
            'Организация работы Совета молодежи',
            'Трек вовлеченности МС',
            'Анкета кандидата',
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def youth_council_development(message: types.Message) -> types.Message:
        buttons = [
            'НТК МС',
            'СЛЕТ МС',
            'Проект "Моя история успеха"',
            '🔙 вернуться в раздел Молодежная политика',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            "⬇ Развитие молодых специалистов",
            reply_markup=markup,
        )

    @staticmethod
    def my_success_story(message: types.Message) -> types.Message:
        buttons = [
            ["перейти в канал", "https://t.me/+PLTbNYqNnCszZjNi"]
        ]
        markup = Buttons.create_inline_keyboard(buttons)
        bot.send_message(
            message.from_user.id,
            'Телеграм канал проекта "Моя история успеха"',
            reply_markup=markup,
        )

    @staticmethod
    def scientific_technical_conference(message: types.Message) -> types.Message:
        bot.send_message(message.from_user.id, ABOUT_NTK)
        parrent_path = ('prod_data/Молодежная_политика/Развитие_молодых_специалистов/НТК/')
        documents = (
            f'{parrent_path}Заявка_Шаблон.docx',
            f'{parrent_path}Шаблон_одностраничника.pptx',
            f'{parrent_path}Шаблон_презентации.pptx',
            f'{parrent_path}dk.pdf',
        )
        captions = (
            'Заявка - Шаблон',
            'Шаблон одностраничника',
            'Шаблон презентации',
            'Дорожная карта',
        )
        Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def youth_council_meeting(message: types.Message) -> types.Message:
        document = (
            'prod_data/Молодежная_политика/Развитие_молодых_специалистов/Слет_МС/Слет_МС.pdf',
        )
        caption = ('Слет МС',)
        Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def youth_council_structure(message: types.Message) -> types.Message:
        document = (
            'prod_data/Молодежная_политика/MS/Структура/structuraMS.pdf',
        )
        caption = ('Структура МС',)
        Documents.send_document_with_markup(message.chat.id, document, caption)
