from telebot import types


class Buttons:

    # Функция для создания кнопок
    @staticmethod
    def create_keyboard_buttons(
            buttons: list[str], row_width: int
    ) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=row_width
        )
        array = []
        for button_text in buttons:
            array.append(types.KeyboardButton(button_text))
        markup.add(*array)
        return markup
