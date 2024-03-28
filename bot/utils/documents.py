from telebot import types
from bot import bot


class Documents:

    @staticmethod
    # Функция для отправки документов
    def send_document_with_markup(
            chat_id: int,
            document: str,
            caption: str,
            markup: types.ReplyKeyboardMarkup,
    ) -> types.Message:
        with open(document, 'rb') as file:
            bot.send_document(
                chat_id,
                file,
                caption,
                parse_mode="html",
                reply_markup=markup,
            )
