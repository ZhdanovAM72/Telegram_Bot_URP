from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ES, ITS, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/time_tracking/government_duties/"
GOVERNMENT_DUTIES = "Исполнение гос.обязанностей"
APPLICATION_STATE_PUBLIC_DUTIES = ("Ш-14.03.05-03 Заявление об исполнении "
                                   "государственных или общественных обязанностей")


class GovernmentDuties:

    @staticmethod
    def government_duties_main(message: types.Message) -> types.Message:
        buttons = [
            f'Исполнение гос.обязанностей {ES}',
            f'Исполнение гос.обязанностей {ST}',
            f'Исполнение гос.обязанностей {ITS}',
            f'Исполнение гос.обязанностей {NNGGF}',
            '🔙 вернуться в раздел Учет рабочего времени',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            "Исполнение гос.обязанностей",
            reply_markup=markup,
        )

    @staticmethod
    def government_duties_es(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ES/main.docx',)
        caption = (APPLICATION_STATE_PUBLIC_DUTIES,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def government_duties_its(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ITS/main.docx',)
        caption = (APPLICATION_STATE_PUBLIC_DUTIES,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def government_duties_nnggf(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}NNGGF/main.docx',)
        caption = (APPLICATION_STATE_PUBLIC_DUTIES,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def government_duties_st(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ST/main.docx',)
        caption = (APPLICATION_STATE_PUBLIC_DUTIES,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
