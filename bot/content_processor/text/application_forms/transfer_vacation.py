from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/vacation_registration/transfer_vacation/"
TRANSFER_EXTENSION_VACATION = "Перенос, продление отпуска"
APPLICATION_TRANSFER_VACATION = "Ш-14.03.06-05 Заявление о переносе отпуска"
MEMO_RESCHEDULING_VACATION = "Ш-14.03.06-06 Служебная записка о переносе отпуска"
APPLICATION_EXTENSION_TRANSFER_LEAVE = (
    "Ш-14.03.06-30 Заявление о продлении-переносе отпуска в связи с временной нетрудоспособностью"
)
APPLICATION_ANOTHER_TYPE_LEAVE = "Ш-14.03.06-07 Заявление о предоставлении иного вида отпуска"


class TransferExtensionVacation:

    @staticmethod
    def transfer_extension_vacation_main(message: types.Message) -> types.Message:
        buttons = [
            f'{TRANSFER_EXTENSION_VACATION} {ES}',
            f'{TRANSFER_EXTENSION_VACATION} {NR}',
            f'{TRANSFER_EXTENSION_VACATION} {ST}',
            f'{TRANSFER_EXTENSION_VACATION} {ITS}',
            f'{TRANSFER_EXTENSION_VACATION} {NNGGF}',
            '🔙 вернуться в раздел Оформление отпусков',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            TRANSFER_EXTENSION_VACATION,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def transfer_extension_vacation_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/application.doc", "rb"),
                "caption": APPLICATION_TRANSFER_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/SZ.doc", "rb"),
                "caption": APPLICATION_EXTENSION_TRANSFER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/health.doc", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def transfer_extension_vacation_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/application.doc", "rb"),
                "caption": APPLICATION_TRANSFER_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/SZ.doc", "rb"),
                "caption": APPLICATION_EXTENSION_TRANSFER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/health.doc", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def transfer_extension_vacation_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/application.doc", "rb"),
                "caption": APPLICATION_TRANSFER_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/SZ.doc", "rb"),
                "caption": APPLICATION_EXTENSION_TRANSFER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/health.doc", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def transfer_extension_vacation_nr(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NR/application.docx", "rb"),
                "caption": APPLICATION_TRANSFER_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}NR/health.docx", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def transfer_extension_vacation_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/application.doc", "rb"),
                "caption": APPLICATION_TRANSFER_VACATION,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/SZ.doc", "rb"),
                "caption": APPLICATION_EXTENSION_TRANSFER_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/dop.doc", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/health.doc", "rb"),
                "caption": APPLICATION_ANOTHER_TYPE_LEAVE,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)
