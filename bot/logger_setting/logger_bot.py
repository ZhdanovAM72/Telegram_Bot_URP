import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = 'bot_log.txt'  # Имя файла логов


def init_logger() -> logging.Logger:
    """Определяем настройки логгера."""
    logging.basicConfig(
        format=('%(asctime)s - %(levelname)s - %(module)s - '
                'строка: %(lineno)d - %(message)s'),
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=500_000,
                backupCount=5
            )
        ],
    )
    return logging.getLogger(__name__)


logger = init_logger()


def log_user_command(message):
    """Логгирование команд пользователей."""
    log_message = (
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    logger.info(log_message)


def log_user_command_updated(message):
    """Логгирование команд пользователей."""
    log_message = (
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    return log_message


def log_photo(message):
    """Логгирование изображений в чате."""
    log_message = (
        f'изображение - {message.photo[0]} '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    return log_message


def log_sticker(message):
    """Логгирование стикеров в чате."""
    log_message = (
        f'изображение {message.sticker} - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    return log_message
