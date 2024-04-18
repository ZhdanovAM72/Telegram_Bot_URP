from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/termination_contract/"
TERMINATION_CONTRACT = "Прекращение ТД"
DISMISSAL_FORM = "Ш-14.03.03-01 Анкета при увольнении"
LETTER_RESIGNATION = "Ш-14.03.03-02 Заявление об увольнении"
APPLICATION_LEAVE_DISMISSAL = "Ш-14.03.06-07 Заявление о предоставлении отпуска с увольнением"


class TerminationEmploymentContract:

    @staticmethod
    def termination_contract_main(message: types.Message) -> types.Message:
        buttons = [
            f'{TERMINATION_CONTRACT} {ES}',
            f'{TERMINATION_CONTRACT} {NR}',
            f'{TERMINATION_CONTRACT} {ST}',
            f'{TERMINATION_CONTRACT} {ITS}',
            f'{TERMINATION_CONTRACT} {NNGGF}',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            TERMINATION_CONTRACT,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def termination_contract_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/questionnaire.doc", "rb"),
                "caption": DISMISSAL_FORM,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/application.doc", "rb"),
                "caption": LETTER_RESIGNATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def termination_contract_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/questionnaire.doc", "rb"),
                "caption": DISMISSAL_FORM,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/application.doc", "rb"),
                "caption": LETTER_RESIGNATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def termination_contract_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/questionnaire.doc", "rb"),
                "caption": DISMISSAL_FORM,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/application.doc", "rb"),
                "caption": LETTER_RESIGNATION,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def termination_contract_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/questionnaire.doc", "rb"),
                "caption": DISMISSAL_FORM,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/application.doc", "rb"),
                "caption": LETTER_RESIGNATION,
            },
        )
        document = (f"{PARRENT_PATH}ST/raspiska.docx",)
        caption = ("Расписка при увольнении",)
        return (Documents.send_media_group_without_markup(message.chat.id, documents),
                Documents.send_document_with_markup(message.chat.id, document, caption))

    @staticmethod
    @contextmanager
    def termination_contract_nr(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NR/otpravka_trudovoi.doc", "rb"),
                "caption": "Заявление на отправку трудовой книжки",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/perevod.doc", "rb"),
                "caption": "Заявление об увольнении в порядке перевода",
            },
            {
                "file": open(f"{PARRENT_PATH}NR/uvolnenie.doc", "rb"),
                "caption": LETTER_RESIGNATION,
            },
            {
                "file": open(f"{PARRENT_PATH}NR/otpusk_uvolnenie.doc", "rb"),
                "caption": APPLICATION_LEAVE_DISMISSAL,
            },
        )
        document = (f"{PARRENT_PATH}NR/cancel.docx",)
        caption = ("Отзыв увольнения",)
        return (Documents.send_media_group_without_markup(message.chat.id, documents),
                Documents.send_document_with_markup(message.chat.id, document, caption))
