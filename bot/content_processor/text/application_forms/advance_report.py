from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/avansov/"
BLANK_CAPTION = "Бланк авансового отчета"
BLANKS = "Бланки"


class AdvanceReport:

    @staticmethod
    def advance_report(message: types.Message) -> types.Message:
        buttons = [
            f'{BLANKS} {ES}',
            f'{BLANKS} {NR}',
            f'{BLANKS} {ST}',
            f'{BLANKS} {ITS}',
            f'{BLANKS} {NNGGF}',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.chat.id,
            'Авансовый отчет',
            reply_markup=markup,
        )

    @staticmethod
    def forms_es(message: types.Message) -> types.Message:
        documents = (
            f'{PARRENT_PATH}ES/blank.doc',
            f'{PARRENT_PATH}ES/info.docx',
        )
        captions = (
            BLANK_CAPTION,
            'Инструкция по заполнению АО',
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def forms_nr(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}NR/SOP.pdf',)
        caption = ('СОП по оформлению отчета по командировке с 01.10.23',)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def forms_its(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ITS/blank_1.xls',)
        caption = (BLANK_CAPTION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def forms_nnggf(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ITS/blank_2.xls',)
        caption = (BLANK_CAPTION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def forms_st(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ST/blank.doc',)
        caption = (BLANK_CAPTION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
