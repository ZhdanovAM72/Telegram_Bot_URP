import telebot
from telebot import types

import pandas as pd

from bot.bot_command import BaseBotCommands
from bot.content_processor import BaseContentProcessor
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command_updated, logger
from bot.constants import NOT_REGISTERED
from bot.content_processor.base_bot_menu_dict import BASE_MENU_DICT
from bot import bot, STOP_COMMAND
from bot.db.create_new import CreateMethods as Create


@bot.message_handler(commands=['admin'])
def admin(message: telebot.types.Message) -> types.Message | None:
    """"Проверяем права администратора."""
    return BaseBotCommands.admin_commands(message)


@bot.message_handler(commands=['updatecode'])
def update_code(message: telebot.types.Message) -> types.Message | None:
    """Обновляем код в БД."""
    return BaseBotCommands.update_code(message)


@bot.message_handler(commands=['createmoderator'])
def create_moderator(message: telebot.types.Message) -> types.Message | None:
    """Создаем модератора."""
    return BaseBotCommands.create_moderator(message)


@bot.message_handler(commands=['moderator'])
def moderator(message: telebot.types.Message) -> types.Message | None:
    """"Проверяем права модератора."""
    return BaseBotCommands.moderator_commands(message)


@bot.message_handler(
    commands=[
        'deleteuser',
        'deletecode',
    ]
)
def delete_user(message: telebot.types.Message) -> types.Message | None:
    """Удаление пользователей."""
    return BaseBotCommands.delete_user_from_db(message)


@bot.message_handler(commands=['dbinfo'])
def export_db(message: telebot.types.Message) -> types.Message | None:
    """Экспортируем БД."""
    return BaseBotCommands.export_info(message)


@bot.message_handler(
    commands=[
        'createcode_ES',
        'createcode_ST',
        'createcode_NR',
        'createcode_ITS',
    ]
)
def create_code(message: telebot.types.Message) -> types.Message | None:
    """Создаем новый код доступа в БД."""
    return BaseBotCommands.create_code(message)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> types.Message | None:
    """Начало работы в ботом."""
    return BaseBotCommands.start(message)


@bot.message_handler(commands=['code'])
def register_user(message) -> types.Message | None:
    """Определяем права пользователя."""
    return BaseBotCommands.register(message)


@bot.message_handler(
    commands=[
        'updates',
        'massmess',
    ]
)
def mass_info_message(message: types.Message) -> types.Message | None:
    """
    Рассылка информации всем пользователям.
    - updates: для заготовленных обновлений
    - massmess: для любых сообщений (до 500 символов)
    """
    return BaseBotCommands.mass_info_message(message)


@bot.message_handler(commands=[STOP_COMMAND])
def stop(message: telebot.types.Message) -> None:
    """Останавливаем работу бота."""
    return BaseBotCommands.stop_command(message)


@bot.message_handler(commands=["test"])
def test(message: telebot.types.Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Зарегистрироваться')
    bot.send_message(message.chat.id, 'Здравствуйте! Пожалуйста, зарегистрируйтесь.', reply_markup=markup)
    return None


@bot.message_handler(func=lambda message: message.text == 'Зарегистрироваться')
def register_button(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, 'Введите логин (логин от учетной записи до символа "@"):')
    bot.register_next_step_handler(message, login_input)
    return None


def login_input(message: telebot.types.Message) -> None:
    login = message.text.lower()
    if not BaseBotSQLMethods.search_email_in_db(login):
        return bot.send_message(message.chat.id, 'Ошибка поиска логина, загеристрируйтесь повторно!')
    bot.send_message(message.chat.id, 'Введите свой табельный номер:')
    bot.register_next_step_handler(message, lambda msg: password_input(msg, login))
    return None


def password_input(message: telebot.types.Message, login: str) -> None:
    try:
        password = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы! Ошибочный табельный номер!')
        raise 'Error tab_number'
    else:
        if password > 99_999 or password < 1:
            return bot.send_message(message.chat.id, 'Вы не зарегистрированы! Ошибочный табельный номер!')
        if not BaseBotSQLMethods.search_tab_number_in_db(password):
            return bot.send_message(message.chat.id, 'Вы не зарегистрированы! Данный табельный номер занят!')
        if not BaseBotSQLMethods.search_telegram_id_in_db(message.chat.id):
            return bot.send_message(message.chat.id, 'Вы не зарегистрированы! Данный id занят!')
        Create.user_sign_up(email=login, tab_number=password, message=message)
        full_name = BaseBotSQLMethods.search_full_name_in_db(message.chat.id)
        if full_name:
            return bot.send_message(message.chat.id, f'{full_name} - Вы зарегистрированы!')
    return bot.send_message(message.chat.id, 'Ошибка поиска данных...')


@bot.message_handler(commands=['add_users'])
def print_excel(message: telebot.types.Message) -> types.Message | None:
    files_paths = [
        "./develop_files/users_data/es.xlsx",
        "./develop_files/users_data/its.xlsx",
        "./develop_files/users_data/nr.xlsx",
        "./develop_files/users_data/nnggf.xlsx",
        "./develop_files/users_data/st.xlsx",
    ]
    for file in files_paths:
        df = pd.read_excel(file)

        def calculate_fot_sv(row):
            full_name: str = row["ФИО сотр."]
            email: str = row["Логин AD"]
            Create.create_new_email(email=email.lower(), full_name=full_name.title())
            return

        df = df.apply(calculate_fot_sv, axis=1)
    return bot.send_message(message.chat.id, "Upload user info done!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message) -> types.Message | None:
    """
    Главное меню чат-бота с глубокой вложенностью
    и возможностью возврата к предыдущему пункту меню.
    """
    check_user = BaseBotSQLMethods.get_user_access(message.chat.id)
    if check_user is None or check_user[1] != message.chat.id:
        return bot.send_message(message.chat.id, NOT_REGISTERED)

    menu_dict = BASE_MENU_DICT

    if message.text in menu_dict.keys():
        menu_dict.get(message.text)(message)

    else:
        menu_dict.get("Неизвестная команда")(message)

    logger.info(log_user_command_updated(message))
    return None


@bot.message_handler(content_types=['photo'])
def user_photo(message: telebot.types.Message) -> types.Message | None:
    """Ловим отправленные пользователем изобращения."""
    return BaseContentProcessor.get_user_photo(message)


@bot.message_handler(content_types=['sticker'])
def user_stiсker(message: telebot.types.Message) -> types.Message | None:
    """Ловим отправленные пользователем стикеры."""
    return BaseContentProcessor.get_user_stiсker(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
