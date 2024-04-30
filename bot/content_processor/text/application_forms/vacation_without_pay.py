from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/vacation_registration/vacation_without_money/"
VACATION_WITHOUT_PAY = "Отпуск без сохранения зп"
APPLICATION_LEAVE_WITHOUT_PAY = "Ш-14.03.06-21 Заявление о предоставлении отпуска без сохранения заработной платы"


class VacationWithoutPay:

    @staticmethod
    def vacation_without_pay_main(message: types.Message) -> types.Message:
        buttons = [
            f'{VACATION_WITHOUT_PAY} {ES}',
            f'{VACATION_WITHOUT_PAY} {NR}',
            f'{VACATION_WITHOUT_PAY} {ST}',
            f'{VACATION_WITHOUT_PAY} {ITS}',
            f'{VACATION_WITHOUT_PAY} {NNGGF}',
            '🔙 вернуться в раздел Оформление отпусков',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            VACATION_WITHOUT_PAY,
            reply_markup=markup,
        )

    @staticmethod
    def vacation_without_pay_es(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}ES/application.doc",)
        caption = (APPLICATION_LEAVE_WITHOUT_PAY,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def vacation_without_pay_its(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}ITS/application.doc",)
        caption = (APPLICATION_LEAVE_WITHOUT_PAY,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def vacation_without_pay_nnggf(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}NNGGF/application.doc",)
        caption = (APPLICATION_LEAVE_WITHOUT_PAY,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def vacation_without_pay_nr(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}NR/application.docx",)
        caption = (APPLICATION_LEAVE_WITHOUT_PAY,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def vacation_without_pay_st(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}ST/application.doc",)
        caption = (APPLICATION_LEAVE_WITHOUT_PAY,)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
