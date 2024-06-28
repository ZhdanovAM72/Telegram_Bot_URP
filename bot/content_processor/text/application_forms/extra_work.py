from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/TK_RF_changes/dop_work/"
EXTRA_WORK = "Доп. работа"
MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK = "Ш-14.03.02-10 Служебная записка о поручении дополнительной работы"


class ExtraWork:

    @staticmethod
    def extra_work_main(message: types.Message) -> types.Message:
        buttons = [
            f'{EXTRA_WORK} {ES}',
            f'{EXTRA_WORK} {NR}',
            f'{EXTRA_WORK} {ST}',
            f'{EXTRA_WORK} {ITS}',
            f'{EXTRA_WORK} {NNGGF}',
            '🔙 вернуться в раздел Изменение трудового договора',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            EXTRA_WORK,
            reply_markup=markup,
        )

    @staticmethod
    def extra_work_es(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ES/SZ.doc",
        )
        captions = (
            MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def extra_work_its(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/SZ_ITS.doc",
        )
        captions = (
            MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def extra_work_nnggf(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/SZ_NNGGF.doc",
        )
        captions = (
            MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def extra_work_nr(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}NR/SZ.doc",
        )
        captions = (
            MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def extra_work_st(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ST/SZ.doc",
        )
        captions = (
            MEMO_ABOUT_ASSIGNING_ADDITIONAL_WORK,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)
