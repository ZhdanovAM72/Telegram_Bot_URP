import telebot
from telebot import types

from bot import bot
from bot.logger_setting.logger_bot import logger, log_user_command_updated
from bot.utils.check_permission import CheckUserPermission
from bot.utils.buttons import Buttons

START_MESSAGE = (
    'Здравствуйте, <b>{0}</b>!\n'
    'Я расскажу Вам о нефтесервисных активах! '
    'выберите интересующую Вас тему в меню.'
)


class StartBotCommand:

    @staticmethod
    def start(message: telebot.types.Message) -> types.Message | None:
        """Приветствуем пользователя и включаем меню бота."""
        if not CheckUserPermission.check_user(message):
            logger.warning(log_user_command_updated(message))
            return None

        if (message.from_user.first_name is not None
           and message.from_user.last_name is not None):
            user_info = (
                f'{message.from_user.first_name} {message.from_user.last_name}'
            )

        elif (message.from_user.first_name is not None
              and message.from_user.last_name is None):
            user_info = message.from_user.first_name

        elif message.from_user.username is not None:
            user_info = message.from_user.username

        else:
            user_info = 'сотрудник'

        buttons = (
            'Информация о боте',
            'Главное меню',
        )
        markup = Buttons.create_keyboard_buttons(buttons)

        logger.info(log_user_command_updated(message))
        return bot.send_message(
            message.chat.id,
            START_MESSAGE.format(user_info),
            parse_mode='html',
            reply_markup=markup,
        )
