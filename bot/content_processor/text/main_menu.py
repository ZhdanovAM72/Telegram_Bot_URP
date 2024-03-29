from telebot import types
from bot.utils.buttons import Buttons
from bot import bot


class MainMenu:

    def main_menu(message: types.Message) -> types.Message:
        buttons = [
            'О компании',
            'Адаптация',
            'Карьерное развитие',
            'Цикл управления талантами',
            'Стажировка',
            'ДМС и РВЛ',
            'Молодежная политика',
            'Бланки заявлений',
            'Планирование закупок',
            'Обратная связь',
        ]
        markup = Buttons.create_keyboard_buttons(buttons, row_width=2)
        bot.send_message(
            message.from_user.id,
            text='Добро пожаловать в главное меню чат-бота \nВыберите интересующий вас раздел',
            reply_markup=markup,
        )
