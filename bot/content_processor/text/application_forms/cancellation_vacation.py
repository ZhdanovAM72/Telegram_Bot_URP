from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/vacation_registration/cancellation/"
CANCELLATION_RECALL_VACATION = "Отмена, отзыв из отпуска"
MEMO_RECALL_FROM_VACATION = "Ш-14.03.06-08 Служебная записка об отзыве из отпуска"
MEMO_VACATION_CANCELLATION = "Ш-14.03.06-10 Служебная записка об отмене отпуска"
APPLICATION_CANCELLATION_VACATION = "Ш-14.03.06-11 Заявление об отмене отпуска"


class CancellationRecallVacation:

    @staticmethod
    def cancellation_recall_vacation_main(message: types.Message) -> types.Message:
        buttons = [
            f'{CANCELLATION_RECALL_VACATION} {ES}',
            f'{CANCELLATION_RECALL_VACATION} {NR}',
            f'{CANCELLATION_RECALL_VACATION} {ST}',
            f'{CANCELLATION_RECALL_VACATION} {ITS}',
            f'{CANCELLATION_RECALL_VACATION} {NNGGF}',
            '🔙 вернуться в раздел Оформление отпусков',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            CANCELLATION_RECALL_VACATION,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def cancellation_recall_vacation_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/SZ_otziv.doc", "rb"),
                "caption": MEMO_RECALL_FROM_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/SZ_otmena.doc", "rb"),
                "caption": MEMO_VACATION_CANCELLATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/application.doc", "rb"),
                "caption": APPLICATION_CANCELLATION_VACATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def cancellation_recall_vacation_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/SZ_otziv.doc", "rb"),
                "caption": MEMO_RECALL_FROM_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/SZ_otmena.doc", "rb"),
                "caption": MEMO_VACATION_CANCELLATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/application.doc", "rb"),
                "caption": APPLICATION_CANCELLATION_VACATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def cancellation_recall_vacation_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/SZ_otziv.doc", "rb"),
                "caption": MEMO_RECALL_FROM_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/SZ_otmena.doc", "rb"),
                "caption": MEMO_VACATION_CANCELLATION,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/application.doc", "rb"),
                "caption": APPLICATION_CANCELLATION_VACATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def cancellation_recall_vacation_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/SZ_otziv.doc", "rb"),
                "caption": MEMO_RECALL_FROM_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/SZ_otmena.doc", "rb"),
                "caption": MEMO_VACATION_CANCELLATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/application.doc", "rb"),
                "caption": APPLICATION_CANCELLATION_VACATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    def cancellation_recall_vacation_nr(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}NR/SZ_otziv.docx",
            f"{PARRENT_PATH}NR/SZ_otmena.doc",
        )
        captions = (
            MEMO_RECALL_FROM_VACATION,
            MEMO_VACATION_CANCELLATION,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)
