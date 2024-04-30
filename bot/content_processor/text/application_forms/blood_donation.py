from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/vacation_registration/blood/"
BLOOD_DONATION = "Сдача крови"
RELEASE_FROM_WORK = "Ш-14.03.06-23 Заявление об освобождении от работы в день сдачи крови"
ANOTHER_DAY_REST = "Ш-14.03.06-24 Заявление о предоставлении другого дня отдыха в связи со сдачей крови"
ADDITIONAL_DAY_REST = "Ш-14.03.06-26 Заявление о предоставлении дополнительного дня отдыха в связи со сдачей крови"


class BloodDonation:

    @staticmethod
    def blood_donation_main(message: types.Message) -> types.Message:
        buttons = [
            f'{BLOOD_DONATION} {ES}',
            f'{BLOOD_DONATION} {NR}',
            f'{BLOOD_DONATION} {ST}',
            f'{BLOOD_DONATION} {ITS}',
            f'{BLOOD_DONATION} {NNGGF}',
            '🔙 вернуться в раздел Оформление отпусков',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            BLOOD_DONATION,
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def blood_donation_es(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ES/osvobodit.doc", "rb"),
                "caption": RELEASE_FROM_WORK,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/drugoi.doc", "rb"),
                "caption": ANOTHER_DAY_REST,
            },
            {
                "file": open(f"{PARRENT_PATH}ES/dop.doc", "rb"),
                "caption": ADDITIONAL_DAY_REST,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def blood_donation_its(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ITS/osvobodit.doc", "rb"),
                "caption": RELEASE_FROM_WORK,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/drugoi.doc", "rb"),
                "caption": ANOTHER_DAY_REST,
            },
            {
                "file": open(f"{PARRENT_PATH}ITS/dop.doc", "rb"),
                "caption": ADDITIONAL_DAY_REST,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def blood_donation_nnggf(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NNGGF/osvobodit.doc", "rb"),
                "caption": RELEASE_FROM_WORK,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/drugoi.doc", "rb"),
                "caption": ANOTHER_DAY_REST,
            },
            {
                "file": open(f"{PARRENT_PATH}NNGGF/dop.doc", "rb"),
                "caption": ADDITIONAL_DAY_REST,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def blood_donation_st(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}ST/osvobodit.doc", "rb"),
                "caption": RELEASE_FROM_WORK,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/drugoi.doc", "rb"),
                "caption": ANOTHER_DAY_REST,
            },
            {
                "file": open(f"{PARRENT_PATH}ST/dop.doc", "rb"),
                "caption": ADDITIONAL_DAY_REST,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def blood_donation_nr(message: types.Message) -> types.Message:
        documents = (
            {
                "file": open(f"{PARRENT_PATH}NR/drugoi.doc", "rb"),
                "caption": ANOTHER_DAY_REST,
            },
            {
                "file": open(f"{PARRENT_PATH}NR/dop.doc", "rb"),
                "caption": ADDITIONAL_DAY_REST,
            },
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)
