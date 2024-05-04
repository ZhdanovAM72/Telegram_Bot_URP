from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/vacation_registration/other_vacation/"
OTHER_TYPES_VACATION = "Другие виды отпусков"
APPLICATION_ANOTHER_LEAVE = "Ш-14.03.06-07 Заявление о предоставлении иного вида отпуска"
APPLICATION_UNSCHEDULED_LEAVE = "Ш-14.03.06-29 Заявление о предоставлении внепланового отпуска"


class OtherTypesVacation:

    @staticmethod
    def other_types_vacation_main(message: types.Message) -> types.Message:
        buttons = [
            f'{OTHER_TYPES_VACATION} {ES}',
            f'{OTHER_TYPES_VACATION} {NR}',
            f'{OTHER_TYPES_VACATION} {ST}',
            f'{OTHER_TYPES_VACATION} {ITS}',
            f'{OTHER_TYPES_VACATION} {NNGGF}',
            '🔙 вернуться в раздел Оформление отпусков',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            OTHER_TYPES_VACATION,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def other_types_vacation_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/dop.doc", "rb"),
                "caption": APPLICATION_ANOTHER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/main.doc", "rb"),
                "caption": APPLICATION_UNSCHEDULED_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def other_types_vacation_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/dop.doc", "rb"),
                "caption": APPLICATION_ANOTHER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/main.doc", "rb"),
                "caption": APPLICATION_UNSCHEDULED_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def other_types_vacation_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/dop.doc", "rb"),
                "caption": APPLICATION_ANOTHER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/main.doc", "rb"),
                "caption": APPLICATION_UNSCHEDULED_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def other_types_vacation_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/dop.doc", "rb"),
                "caption": APPLICATION_UNSCHEDULED_LEAVE,
            },

        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def other_types_vacation_nr(message: types.Message) -> types.Message:
        documents_docx = (
            {
                "file": open(f"{PARRENT_PATH}NR/weekend.docx", "rb"),
                "caption": "Заявление на предоставление дня отдыха за РВД в командировке.",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/moving.docx", "rb"),
                "caption": "Ш-05.08-07 Заявление на присоединение выходных дней",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/dop.docx", "rb"),
                "caption": "Ш-14.03.06-07 Заявление о предоставлении иного вида отпуска",
            },

        )
        documents_doc = (
            {
                "file": open(f"{PARRENT_PATH}NR/family.doc", "rb"),
                "caption": "Заявление о предоставлении отпуска",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/arrangement.doc", "rb"),
                "caption": "Ш-14.03.06-07 Заявление о предоставлении иного вида отпуска ОБУСТРОЙСТВО",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/dop_2.doc", "rb"),
                "caption": "Ш-14.03.06-07 Заявление о предоставлении доп. дней отпуска",
            },

        )
        return (Documents.send_media_group_without_markup(message.chat.id, documents_docx),
                Documents.send_media_group_without_markup(message.chat.id, documents_doc))
