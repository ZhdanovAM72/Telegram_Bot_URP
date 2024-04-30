from contextlib import contextmanager

from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/time_tracking/change_shedule/"
CHANGE_SCHEDULE = "Изменение графика"
APPLICATION_SCHEDULE_CHANGE = "Ш-14.03.05-02 Заявление об изменении графика работы персонала"
APPLICATION_EARLY_LEAVE = "Ш-14.03.05-04 Заявление о досрочном выходе из отпуска по уходу за ребенком"
CHANGING_STAFF_SCHEDULE = "Ш-14.03.05-13 Служебная записка об изменении графика работы персонала"
NEW_STAFF_SCHEDULE = "Ш-14.03.05-14 Служебная записка о необходимости формирования нового графика работы персонала"
CHANGING_WORKING_HOURS = "Ш-14.03.02-03 Заявление об изменении режима рабочего времени"


class WorkSchedule:

    @staticmethod
    def work_schedule_main(message: types.Message) -> types.Message:
        buttons = [
            f'{CHANGE_SCHEDULE} {ES}',
            f'{CHANGE_SCHEDULE} {NR}',
            f'{CHANGE_SCHEDULE} {ST}',
            f'{CHANGE_SCHEDULE} {ITS}',
            f'{CHANGE_SCHEDULE} {NNGGF}',
            '🔙 вернуться в раздел Учет рабочего времени',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            'Изменение графика работы',
            reply_markup=markup,
        )

    @staticmethod
    @contextmanager
    def change_schedule_es(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ES/main.docx", "rb"), "caption": APPLICATION_SCHEDULE_CHANGE},
            {"file": open(f"{PARRENT_PATH}ES/baby_cancel.docx", "rb"), "caption": APPLICATION_EARLY_LEAVE},
            {"file": open(f"{PARRENT_PATH}ES/change.docx", "rb"), "caption": CHANGING_STAFF_SCHEDULE},
            {"file": open(f"{PARRENT_PATH}ES/new.docx", "rb"), "caption": NEW_STAFF_SCHEDULE},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def change_schedule_its(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ITS/main.docx", "rb"), "caption": APPLICATION_SCHEDULE_CHANGE},
            {"file": open(f"{PARRENT_PATH}ITS/baby_cancel.docx", "rb"), "caption": APPLICATION_EARLY_LEAVE},
            {"file": open(f"{PARRENT_PATH}ITS/change.docx", "rb"), "caption": CHANGING_STAFF_SCHEDULE},
            {"file": open(f"{PARRENT_PATH}ITS/new.docx", "rb"), "caption": NEW_STAFF_SCHEDULE},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def change_schedule_st(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}ST/main.docx", "rb"), "caption": APPLICATION_SCHEDULE_CHANGE},
            {"file": open(f"{PARRENT_PATH}ST/baby_cancel.docx", "rb"), "caption": APPLICATION_EARLY_LEAVE},
            {"file": open(f"{PARRENT_PATH}ST/change.docx", "rb"), "caption": CHANGING_STAFF_SCHEDULE},
            {"file": open(f"{PARRENT_PATH}ST/new.docx", "rb"), "caption": NEW_STAFF_SCHEDULE},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def change_schedule_nnggf(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}NNGGF/main.docx", "rb"), "caption": APPLICATION_SCHEDULE_CHANGE},
            {"file": open(f"{PARRENT_PATH}NNGGF/change.docx", "rb"), "caption": CHANGING_STAFF_SCHEDULE},
            {"file": open(f"{PARRENT_PATH}NNGGF/new.docx", "rb"), "caption": NEW_STAFF_SCHEDULE},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)

    @staticmethod
    @contextmanager
    def change_schedule_nr(message: types.Message) -> types.Message:
        documents = (
            {"file": open(f"{PARRENT_PATH}NR/main.docx", "rb"), "caption": APPLICATION_SCHEDULE_CHANGE},
            {"file": open(f"{PARRENT_PATH}NR/change_grafik.docx", "rb"), "caption": CHANGING_WORKING_HOURS},
        )
        return Documents.send_media_group_without_markup(message.chat.id, documents)
