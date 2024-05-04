from telebot import types

from bot import bot
from bot.bot_command.start import StartBotCommand
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command_updated, logger


class RegisterUserCommand:

    @classmethod
    def register(cls, message: types.Message) -> None:
        """Определяем права пользователя."""
        input_code = message.text
        erorr_code_message = (
            'Команда использована неверно, '
            'введите код как показано на примере!\n'
            'Пример: \n/code jifads9af8@!1'
        )
        if input_code == '/code':
            logger.warning(log_user_command_updated(message))
            return bot.send_message(
                message.chat.id,
                erorr_code_message,
            )

        clear_code = input_code.split()
        if len(clear_code) <= 1 or len(clear_code) > 2:
            logger.warning(log_user_command_updated(message))
            return bot.send_message(
                message.chat.id,
                erorr_code_message,
            )

        check = BaseBotSQLMethods.search_code_in_db(clear_code[1])
        if check[1] is not None:
            logger.warning(log_user_command_updated(message))
            return bot.send_message(message.chat.id, 'Данный код занят!')
        elif check is not None and check[0] == clear_code[1]:
            logger.info(log_user_command_updated(message))
            bot.send_message(message.chat.id, 'Код найден в базе!')
            BaseBotSQLMethods.create_new_user(
                clear_code[1],
                message.from_user.username,
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
            )
            return StartBotCommand.start(message)

        logger.warning(log_user_command_updated(message))
        return bot.send_message(
            message.chat.id,
            'Код не найден в системе!\n'
            'Запросите код у администратора проекта, '
            'либо используйте имеющийся.',
        )
