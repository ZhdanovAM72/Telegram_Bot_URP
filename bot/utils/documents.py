from telebot import types
from bot import bot


class Documents:

    @staticmethod
    # Функция для отправки документов по одному
    def send_document_with_markup(
            chat_id: int,
            document: list[str] | tuple[str],
            caption: list[str] | tuple[str] = None,
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

    @staticmethod
    # Функция для отправки документов группой
    def send_media_group_without_markup(
            chat_id: int,
            documents: list[dict] | tuple[dict],
    ) -> types.Message:
        input_media_documents = [
            types.InputMediaDocument(
                file['file'],
                caption=file['caption'],
                parse_mode="html",
            ) for file in documents
        ]
        bot.send_media_group(chat_id, input_media_documents)
