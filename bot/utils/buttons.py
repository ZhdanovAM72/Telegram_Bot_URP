from telebot import types


class Buttons:

    @staticmethod
    def create_keyboard_buttons(
            buttons: list[str] | tuple[str], row_width: int = 3
    ) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            row_width=row_width,
        )
        array = []
        for button_text in buttons:
            array.append(types.KeyboardButton(button_text))
        markup.add(*array)
        return markup

    @staticmethod
    def create_inline_keyboard(
            buttons: list[list[str]] | tuple[tuple[str]],
            row_width: int = 3,
            callback: bool = False
    ) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=row_width)
        array = []
        for button_value in buttons:
            if not callback:
                array.append(
                    types.InlineKeyboardButton(
                        text=button_value[0],
                        url=button_value[1],
                    )
                )
            else:
                array.append(
                    types.InlineKeyboardButton(
                        text=button_value[0],
                        callback_data=button_value[1],
                    )
                )
        markup.add(*array)
        return markup
