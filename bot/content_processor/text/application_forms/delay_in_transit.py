from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ES, ITS, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/time_tracking/delay_in_transit/"
DOWNTIME_AND_DELAY = "Простой, задержка в пути"
MEMO_ABOUT_DOWNTIME = ("Ш-14.03.05-16 Служебная записка о простое "
                       "/незапланированном простое, содержащая список работников")
LIST_OF_EMPLOYEES = "Ш-14.03.05-17 Список работников, которым необходимо оформить задержку в пути"


class DelayTransit:

    @staticmethod
    def delay_it_transit_main(message: types.Message) -> types.Message:
        buttons = [
            f'{DOWNTIME_AND_DELAY} {ES}',
            f'{DOWNTIME_AND_DELAY} {ST}',
            f'{DOWNTIME_AND_DELAY} {ITS}',
            f'{DOWNTIME_AND_DELAY} {NNGGF}',
            '🔙 вернуться в раздел Учет рабочего времени',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            "Простой, задержка в пути",
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def delay_it_transit_es(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ES/SZ.docx", "rb"), "caption": MEMO_ABOUT_DOWNTIME},
            {"file": open(f"{PARRENT_PATH}ES/list.docx", "rb"), "caption": LIST_OF_EMPLOYEES},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def delay_it_transit_its(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ITS/SZ.docx", "rb"), "caption": MEMO_ABOUT_DOWNTIME},
            {"file": open(f"{PARRENT_PATH}ITS/list.docx", "rb"), "caption": LIST_OF_EMPLOYEES},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def delay_it_transit_nnggf(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}NNGGF/SZ.docx", "rb"), "caption": MEMO_ABOUT_DOWNTIME},
            {"file": open(f"{PARRENT_PATH}NNGGF/list.docx", "rb"), "caption": LIST_OF_EMPLOYEES},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def delay_it_transit_st(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ST/SZ.docx", "rb"), "caption": MEMO_ABOUT_DOWNTIME},
            {"file": open(f"{PARRENT_PATH}ST/list.docx", "rb"), "caption": LIST_OF_EMPLOYEES},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)
