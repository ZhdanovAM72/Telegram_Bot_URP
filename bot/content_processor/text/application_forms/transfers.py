from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/TK_RF_changes/transfers/"
TRANSFERS = "Переводы"
APPLICATION_TRANSFER_ANOTHER_JOB = "Ш-14.03.02-01 Заявление о переводе на другую работу"
MEMO_ABOUT_TRANSFER_ANOTHER_JOB = "Ш-14.03.02-07 Служебная записка о переводе на другую работу"
ANOTHER_JOB_PREGNANCY = "Ш-14.03.02-15 Заявление о переводе на другую работу в связи с беременностью"


class Transfers:

    @staticmethod
    def transfers_main(message: types.Message) -> types.Message:
        buttons = [
            f'{TRANSFERS} {ES}',
            f'{TRANSFERS} {NR}',
            f'{TRANSFERS} {ST}',
            f'{TRANSFERS} {ITS}',
            f'{TRANSFERS} {NNGGF}',
            '🔙 вернуться в раздел Изменение трудового договора',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            TRANSFERS,
            reply_markup=markup,
        )

    @staticmethod
    def transfers_es(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ES/application.doc",
            f"{PARRENT_PATH}ES/SZ.docx",
            f"{PARRENT_PATH}ES/application_health_risk_work.doc",
        )
        captions = (
            APPLICATION_TRANSFER_ANOTHER_JOB,
            MEMO_ABOUT_TRANSFER_ANOTHER_JOB,
            ANOTHER_JOB_PREGNANCY,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def transfers_its(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/ITS_application.doc",
            f"{PARRENT_PATH}ITS/ITS_SZ.docx",
            f"{PARRENT_PATH}ITS/ITS_application_health_risk_work.doc",
        )
        captions = (
            APPLICATION_TRANSFER_ANOTHER_JOB,
            MEMO_ABOUT_TRANSFER_ANOTHER_JOB,
            ANOTHER_JOB_PREGNANCY,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def transfers_nnggf(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/NNGGF_application.doc",
            f"{PARRENT_PATH}ITS/NNGGF_SZ.docx",
            f"{PARRENT_PATH}ITS/NNGGF_application_health_risk_work.doc",
        )
        captions = (
            APPLICATION_TRANSFER_ANOTHER_JOB,
            MEMO_ABOUT_TRANSFER_ANOTHER_JOB,
            ANOTHER_JOB_PREGNANCY,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def transfers_st(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ST/application.doc",
            f"{PARRENT_PATH}ST/SZ.docx",
        )
        captions = (
            APPLICATION_TRANSFER_ANOTHER_JOB,
            MEMO_ABOUT_TRANSFER_ANOTHER_JOB,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def transfers_nr(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}NR/application.docx",
        )
        captions = (
            APPLICATION_TRANSFER_ANOTHER_JOB,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)
