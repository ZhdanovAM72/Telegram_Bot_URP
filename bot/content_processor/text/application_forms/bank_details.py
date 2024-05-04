from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, NNGGF, ST

PARRENT_PATH = "prod_data/blanks/bank_details/"
BANK_DETAILS = "Банковские реквизиты"
TRANSFER_SALARY_ACCORDING_DETAILS = "Заявление на перечисление ЗП по реквизитам"
ACCEPTANCE_CHANGE_BANK_DETAILS = "Заявление о принятии и смене банка и реквизитов"


class BankDetails:

    @staticmethod
    def bank_details_main(message: types.Message) -> types.Message:
        buttons = [
            f'{BANK_DETAILS} {ES}',
            f'{BANK_DETAILS} {NR}',
            f'{BANK_DETAILS} {ST}',
            f'{BANK_DETAILS} {ITS}',
            f'{BANK_DETAILS} {NNGGF}',
            '🔙 вернуться в раздел Бланки заявлений',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        return bot.send_message(
            message.chat.id,
            BANK_DETAILS,
            reply_markup=markup,
        )

    @staticmethod
    def bank_details_es(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ES/statement.doc",
        )
        captions = (
            TRANSFER_SALARY_ACCORDING_DETAILS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def bank_details_its(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/stateman_ITS.doc",
        )
        captions = (
            TRANSFER_SALARY_ACCORDING_DETAILS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def bank_details_nnggf(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ITS/stateman_NNGGF.doc",
        )
        captions = (
            TRANSFER_SALARY_ACCORDING_DETAILS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def bank_details_nr(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}NR/statement.docx",
        )
        captions = (
            TRANSFER_SALARY_ACCORDING_DETAILS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)

    @staticmethod
    def bank_details_st(message: types.Message) -> types.Message:
        documents = (
            f"{PARRENT_PATH}ST/statement.doc",
        )
        captions = (
            TRANSFER_SALARY_ACCORDING_DETAILS,
        )
        return Documents.send_document_with_markup(message.chat.id, documents, captions)
