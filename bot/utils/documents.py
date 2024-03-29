from telebot import types
from bot import bot


class Documents:

    @staticmethod
    # Функция для отправки документов
    def send_document_with_markup(
            chat_id: int,
            document: list[str],
            caption: list[str] = None,
            markup: types.ReplyKeyboardMarkup = None,
    ) -> types.Message:
        for i in range(len(document)):
            with open(document[i], 'rb') as file:
                bot.send_document(
                    chat_id,
                    file,
                    caption=caption[i],
                    parse_mode="html",
                    reply_markup=markup,
                )
