from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/TK_RF_changes/working_hours/"
WORKING_HOURS = "Режим рабочего времени"
STATEMENT_REDUCING_SERVICE_STANDARDS = "Ш-14.03.02-02 Заявление о снижении норм выработки_норм обслуживания"
APPLICATION_CHANGING_WORKING_HOURS = "Ш-14.03.02-03 Заявление об изменении режима рабочего времени"


class WorkingHours:

    @staticmethod
    def working_hours_main(message: types.Message) -> types.Message:
        buttons = [
            f'{WORKING_HOURS} {ES}',
            f'{WORKING_HOURS} {NR}',
            f'{WORKING_HOURS} {ST}',
            f'{WORKING_HOURS} {ITS}',
            f'{WORKING_HOURS} {NNGGF}',
            '🔙 вернуться в раздел Изменение трудового договора',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            WORKING_HOURS,
            reply_markup=markup,
        )

    @staticmethod
    def working_hours_es(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ES/work_down.doc",
            f"{PARRENT_PATH}ES/change_work_hours.docx",
        )
        captions = (
            STATEMENT_REDUCING_SERVICE_STANDARDS,
            APPLICATION_CHANGING_WORKING_HOURS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def working_hours_its(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/ITS_work_down.doc",
            f"{PARRENT_PATH}ITS/ITS_change_work_hours.docx",
        )
        captions = (
            STATEMENT_REDUCING_SERVICE_STANDARDS,
            APPLICATION_CHANGING_WORKING_HOURS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def working_hours_nnggf(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/NNGGF_work_down.doc",
            f"{PARRENT_PATH}ITS/NNGGF_change_work_hours.docx",
        )
        captions = (
            STATEMENT_REDUCING_SERVICE_STANDARDS,
            APPLICATION_CHANGING_WORKING_HOURS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def working_hours_st(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ST/work_down.doc",
            f"{PARRENT_PATH}ST/change_work_hours.docx",
        )
        captions = (
            STATEMENT_REDUCING_SERVICE_STANDARDS,
            APPLICATION_CHANGING_WORKING_HOURS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def working_hours_nr(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}NR/change_work_hours.docx",)
        caption = (APPLICATION_CHANGING_WORKING_HOURS,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
