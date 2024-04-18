from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constant import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/time_tracking/working_day_off/"
DAY_OFF_WORKING = "Работа в выходной день"
WEEKENDS_WORK_DECISION = (
    "Ш-14.03.05-15 Решение о привлечении к работе в выходные нерабоч. праздничные дни или к сверхур.работе"
)
WEEKENDS_WORK_MEMO = "Служебная записка на привлечение к работе в выходные дни"


class DayOffWorking:

    @staticmethod
    def day_off_working_main(message: types.Message) -> types.Message:
        buttons = [
            f'{DAY_OFF_WORKING} {ES}',
            f'{DAY_OFF_WORKING} {NR}',
            f'{DAY_OFF_WORKING} {ST}',
            f'{DAY_OFF_WORKING} {ITS}',
            f'{DAY_OFF_WORKING} {NNGGF}',
            '🔙 вернуться в раздел Учет рабочего времени',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            DAY_OFF_WORKING,
            reply_markup=markup,
        )

    @staticmethod
    def day_off_working_es(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ES/main.docx',)
        caption = (WEEKENDS_WORK_DECISION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def day_off_working_its(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ITS/main.docx',)
        caption = (WEEKENDS_WORK_DECISION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def day_off_working_nnggf(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}NNGGF/main.docx',)
        caption = (WEEKENDS_WORK_DECISION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def day_off_working_st(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}ST/main.docx',)
        caption = (WEEKENDS_WORK_DECISION,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def day_off_working_nr(message: types.Message) -> types.Message:
        document = (f'{PARRENT_PATH}NR/main.docx',)
        caption = (WEEKENDS_WORK_MEMO,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
