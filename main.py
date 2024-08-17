import os

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


@bot.message_handler(commands=['create_admin'])
def create_admin(message: telebot.types.Message) -> types.Message | None:
    """"Наделяем пользователя правами администратора."""
    return BaseBotCommands.create_admin(message)


@bot.message_handler(commands=['delete_admin'])
def delete_admin(message: telebot.types.Message) -> types.Message | None:
    """"Отзываем права администратора."""
    return BaseBotCommands.delete_admin(message)


@bot.message_handler(commands=['create_moderator'])
def create_moderator(message: telebot.types.Message) -> types.Message | None:
    """Наделяем пользователя правами модератора."""
    return BaseBotCommands.create_moderator(message)


@bot.message_handler(commands=['delete_moderator'])
def delete_moderator(message: telebot.types.Message) -> types.Message | None:
    """"Отзываем права модератора."""
    return BaseBotCommands.delete_moderator(message)


@bot.message_handler(commands=['moderator'])
def moderator(message: telebot.types.Message) -> types.Message | None:
    """"Проверяем права модератора."""
    return BaseBotCommands.moderator_commands(message)


@bot.message_handler(commands=['delete_email'])
def delete_email_user(message: telebot.types.Message) -> types.Message | None:
    """Удаление пользователей."""
    return BaseBotCommands.delete_user_by_email(message)


@bot.message_handler(commands=['dbinfo'])
def export_db(message: telebot.types.Message) -> types.Message | None:
    """Экспортируем БД."""
    return BaseBotCommands.export_info(message)


@bot.message_handler(commands=['logs_info'])
def export_logs(message: telebot.types.Message) -> types.Message | None:
    """Экспортируем БД."""
    return BaseBotCommands.export_logs(message)


@bot.message_handler(commands=['create_user_data,'])
def create_code(message: telebot.types.Message) -> types.Message | None:
    """Создаем новый код доступа в БД."""
    return BaseBotCommands.create_user_data(message)


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


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    return BaseBotCommands.start_command(message)


@bot.callback_query_handler(func=lambda call: call.data == 'start_register')
def register(call: types.CallbackQuery) -> types.Message:
    return BaseBotCommands.register(call)

@bot.message_handler(commands=['add_new_users'])
def wait_for_file(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "Пожалуйста отправьте в чат файл с данными пользоватлей для загрузки в базу данных."
        "\n(максимальный размер файла 20 МБ)",
    )
    bot.register_next_step_handler(message, process_file)

def process_file(message: telebot.types.Message) -> types.Message | None:
    if message.content_type != 'document':
        return bot.send_message(message.chat.id, "Пложалуйста используйте excel файл.")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_path = 'user_data.xlsx'
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    try:
        df = pd.read_excel(file_path)
        logger.info(df)

        def calculate_fot_sv(row):
            full_name: str = row["ФИО сотр."]
            email: str = row["Логин AD"]
            Create.create_new_email(email=email.lower().strip(), full_name=full_name.title())
            return

        df = df.apply(calculate_fot_sv, axis=1)
    except Exception as e:
        logger.info(f'ERROR add_users: {e}')
        return bot.send_message(
            message.chat.id,
            'Ошибка! Пользователи не загружены! Проверьте файл и попробуйте снова!'
            '\n(снова запустите команду и используйте excel файл)'
            '\nСтолбцы должны называться строго "ФИО сотр." и "Логин AD"',
        )

    os.remove(file_path)
    return bot.send_message(message.chat.id, "Пользователи загружены!")


def add_users() -> None:
    files_paths = [
        "./develop_files/users_data/es.xlsx",
        "./develop_files/users_data/its.xlsx",
        "./develop_files/users_data/nr.xlsx",
        "./develop_files/users_data/nnggf.xlsx",
        "./develop_files/users_data/st.xlsx",
    ]
    create_users = Create()
    for file in files_paths:
        df = pd.read_excel(file)

        def calculate_fot_sv(row):
            full_name: str = row["ФИО сотр."]
            email: str = row["Логин AD"]
            create_users.create_new_email(email=email.lower().strip(), full_name=full_name.title())
            return

        df = df.apply(calculate_fot_sv, axis=1)
    logger.info("Upload user info done!")
    return


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message) -> types.Message | None:
    """
    Главное меню чат-бота с глубокой вложенностью
    и возможностью возврата к предыдущему пункту меню.
    """
    check_user = BaseBotSQLMethods.get_user_access(message.chat.id)
    if not check_user:
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
    # add_users()
    # base_bot_commands = BaseBotCommands()
    # base_bot_commands.create_first_admin("gasanbekova.bm")
    # base_bot_commands.create_first_admin("zhdanov.am")
    bot.polling(none_stop=True, interval=1)
