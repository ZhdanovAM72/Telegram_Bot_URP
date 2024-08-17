from telebot import types

from bot import bot
from bot.db import BaseBotSQLMethods
from bot.utils.check_permission import CheckUserPermission
from bot.logger_setting.logger_bot import log_user_command_updated, logger


class CreateCodeCommands:

    @classmethod
    def create_user_data(cls, message: types.Message) -> types.Message | None:
        """Создание кода доступа."""
        if (CheckUserPermission.check_moderator(message)
           or CheckUserPermission.check_admin(message)):
            log_user_command_updated(message)
        else:
            return bot.send_message(message.chat.id, 'Недостаточно прав!')

        user_data = message.text.split(',')
        user_email = user_data[1].strip().lower()
        user_full_name = user_data[2].title()

        created_user = BaseBotSQLMethods.search_email_in_db(user_email)
        if created_user:
            logger.info('Попытка повторной записи email в БД!')
            return bot.send_message(message.chat.id, f'Данный email занят: {user_email}')
        BaseBotSQLMethods.create_new_email(user_email, user_full_name)

        if created_user is None:
            bot.send_message(message.chat.id, 'Непредвиденная ошибка.')
        user_full_name = BaseBotSQLMethods.search_full_name_if_email(user_email)
        return bot.send_message(message.chat.id, f'Данные записаны в бд! Новый пользователь: {user_full_name}')
