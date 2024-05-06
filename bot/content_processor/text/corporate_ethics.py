from telebot import types
from bot.utils.buttons import Buttons
from bot.utils.documents import Documents
from bot import bot
from bot.constants import ES, ITS, NR, ST

CORPORATE_ETHICS = "Корпоративная этика"
PARRENT_PATH = "prod_data/о_компании/corp_ethics/"
MEMO_CONFLICT_RESOLUTION = "Памятка по урегулированию конфликтов в Нефтесервисных активах"
REGULATIONS_CORPORATE_ETHICS_COMMISSION = "Положение о комиссии по Корпоративной этике"


class CorporateEthics:

    @staticmethod
    def corporate_ethics_main(message: types.Message) -> types.Message:
        buttons = [
            f"{CORPORATE_ETHICS} {ES}",
            f"{CORPORATE_ETHICS} {ITS}",
            f"{CORPORATE_ETHICS} {NR}",
            f"{CORPORATE_ETHICS} {ST}",
            "🔙 вернуться в раздел О компании",
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=1)
        bot.send_message(
            message.from_user.id,
            text=f"⬇ {CORPORATE_ETHICS}",
            reply_markup=markup,
        )
        document = (f"{PARRENT_PATH}info.pdf",)
        caption = (f"{MEMO_CONFLICT_RESOLUTION}",)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def corporate_ethics_es(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}es.pdf",)
        caption = (f"{REGULATIONS_CORPORATE_ETHICS_COMMISSION} {ES}",)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def corporate_ethics_its(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}its.pdf",)
        caption = (f"{REGULATIONS_CORPORATE_ETHICS_COMMISSION} {ITS}",)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def corporate_ethics_nr(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}nr.pdf",)
        caption = (f"{REGULATIONS_CORPORATE_ETHICS_COMMISSION} {NR}",)
        return Documents.send_document_with_markup(message.chat.id, document, caption)

    @staticmethod
    def corporate_ethics_st(message: types.Message) -> types.Message:
        document = (f"{PARRENT_PATH}st.pdf",)
        caption = (f"{REGULATIONS_CORPORATE_ETHICS_COMMISSION} {ST}",)
        return Documents.send_document_with_markup(message.chat.id, document, caption)
