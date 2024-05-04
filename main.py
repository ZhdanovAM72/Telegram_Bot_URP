import telebot
from telebot import types

from bot.bot_command import BaseBotCommands
from bot.content_processor import BaseContentProcessor
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command_updated, logger
from bot.constants import NOT_REGISTERED
from bot.content_processor.base_bot_menu_dict import BASE_MENU_DICT
from bot import bot, STOP_COMMAND


@bot.message_handler(commands=['admin'])
def admin(message: telebot.types.Message):
    """"Проверяем права администратора."""
    return BaseBotCommands.admin_commands(message)


@bot.message_handler(commands=['updatecode'])
def update_code(message: telebot.types.Message):
    """Обновляем код в БД."""
    return BaseBotCommands.update_code(message)


@bot.message_handler(commands=['createmoderator'])
def create_moderator(message: telebot.types.Message):
    """Создаем модератора."""
    return BaseBotCommands.create_moderator(message)


@bot.message_handler(commands=['moderator'])
def moderator(message: telebot.types.Message):
    """"Проверяем права модератора."""
    return BaseBotCommands.moderator_commands(message)


@bot.message_handler(
    commands=[
        'deleteuser',
        'deletecode',
    ]
)
def delete_user(message: telebot.types.Message):
    """Удаление пользователей."""
    return BaseBotCommands.delete_user_from_db(message)


@bot.message_handler(commands=['dbinfo'])
def export_db(message: telebot.types.Message):
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
def create_code(message: telebot.types.Message):
    """Создаем новый код доступа в БД."""
    return BaseBotCommands.create_code(message)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    """Начало работы в ботом."""
    return BaseBotCommands.start(message)


@bot.message_handler(commands=['code'])
def register_user(message):
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
def stop(message: telebot.types.Message):
    """Останавливаем работу бота."""
    return BaseBotCommands.stop_command(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message: telebot.types.Message):
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
def user_photo(message: telebot.types.Message):
    """Ловим отправленные пользователем изобращения."""
    return BaseContentProcessor.get_user_photo(message)


@bot.message_handler(content_types=['sticker'])
def user_stiсker(message: telebot.types.Message):
    """Ловим отправленные пользователем стикеры."""
    return BaseContentProcessor.get_user_stiсker(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
