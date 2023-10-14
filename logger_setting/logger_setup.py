from logger_setting.logger_bot import logger

# логгирование команд.
logger.info(
        f'команда: {message.text} - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )

