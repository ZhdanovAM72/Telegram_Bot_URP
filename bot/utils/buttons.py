from telebot import types


class Buttons:

    # Функция для создания кнопок
    @staticmethod
    def create_keyboard_buttons(
            buttons: list, row_with: int
    ) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=row_with
        )
        for button_text in buttons:
            button = types.KeyboardButton(button_text)
            markup.add(button)
        return markup
