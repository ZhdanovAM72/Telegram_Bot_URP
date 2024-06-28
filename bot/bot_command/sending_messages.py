from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import logger, log_user_command_updated
from bot.utils.check_permission import CheckUserPermission
from bot.db import BaseBotSQLMethods
from bot.updates import UPDATE_MESSAGE
from bot.constants import MAX_MESSAGE_SYMBOLS

ERORR_CODE_MESSAGE = (
    'Команда использована неверно, '  # noqa W605
    'введите запрос как показано на примере\!\n'  # noqa W605
    '\nПример\: \n\/massmess *your\_message* \n'  # noqa W605
    f'\nМаксимально *{MAX_MESSAGE_SYMBOLS}* символов\!'  # noqa W605
)


class SendingMessagesBotCommands:

    @staticmethod
    def mass_info_message(message: types.Message) -> types.Message | None:
        """
        Рассылка информации всем пользователям.
        - updates: для заготовленных обновлений
        - massmess: для любых сообщений (до 500 символов)
        """
        if not CheckUserPermission.check_admin(message):
            logger.warning(log_user_command_updated(message))
            return None

        input_message = message.text.split()
        if input_message[0] == '/updates':
            message_for_users = UPDATE_MESSAGE
        elif input_message[0] == '/massmess':
            message_for_users = ' '.join(input_message[1:])

            if (len(input_message) <= 1
               or len(' '.join(input_message[1:])) > MAX_MESSAGE_SYMBOLS):
                logger.warning(log_user_command_updated(message))
                return bot.send_message(
                    message.chat.id,
                    ERORR_CODE_MESSAGE,
                    parse_mode='MarkdownV2',
                )

        users = BaseBotSQLMethods.search_all_users()
        if users is None:
            return bot.send_message(
                message.chat.id,
                ERORR_CODE_MESSAGE,
                parse_mode='MarkdownV2',
            )
        send_count = 0
        eror_count = 0

        for user in users:
            try:
                bot.send_message(
                    chat_id=user.telegram_id,
                    text=message_for_users,
                )
                send_count += 1
            except Exception:
                eror_count += 1
                raise bot.send_message(
                    message.chat.id,
                    f'ошибка отправки пользователю с id № *{user.full_name}*',
                    parse_mode='MarkdownV2',
                )
            finally:
                continue

        logger.info(log_user_command_updated(message))
        return bot.send_message(
            message.chat.id,
            text=(
                f'Сообщение успешно отправлено *{send_count}* пользователям\!\n'  # noqa W605
                f'\nСообщение не доставлено *{eror_count}* пользователям\!'  # noqa W605
            ),
            parse_mode='MarkdownV2',
        )
