from telebot import types

from bot import bot
from bot.bot_command.start import StartBotCommand
from bot.db import BaseBotSQLMethods
from bot.logger_setting.logger_bot import log_user_command


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
            bot.send_message(
                message.chat.id,
                erorr_code_message,
            )
            return log_user_command(message)

        clear_code = input_code.split()
        if len(clear_code) <= 1 or len(clear_code) > 2:
            bot.send_message(
                message.chat.id,
                erorr_code_message,
            )
            return log_user_command(message)

        check = BaseBotSQLMethods.search_code_in_db(clear_code[1])
        if check[1] is not None:
            return bot.send_message(message.chat.id, 'Данный код занят!')
        elif check is not None and check[0] == clear_code[1]:
            bot.send_message(message.chat.id, 'Код найден в базе!')
            BaseBotSQLMethods.create_new_user(
                clear_code[1],
                message.from_user.username,
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
            )
            return StartBotCommand.start(message)

        bot.send_message(
            message.chat.id,
            'Код не найден в системе!\n'
            'Запросите код у администратора проекта, '
            'либо используйте имеющийся.',
        )
        return log_user_command(message)
