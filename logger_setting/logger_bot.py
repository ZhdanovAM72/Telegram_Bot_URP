import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = 'bot_log.txt'  # Имя файла логов


def init_logger() -> logging.Logger:
    """Определяем настройки логгера."""
    logging.basicConfig(
        format=('%(asctime)s - %(levelname)s - %(name)s - '
                'строка: %(lineno)d - %(message)s'),
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=5_000_000,
                backupCount=5
            )
        ],
    )
    return logging.getLogger(__name__)


logger = init_logger()


def log_user_command(message):
    """Логгирование команд."""
    log_message = logger.info(
        f'команда: "{message.text}" - '
        f'пользователь: {message.from_user.username} - '
        f'id пользователя: {message.chat.id} - '
        f'имя: {message.from_user.first_name} - '
        f'фамилия: {message.from_user.last_name}'
    )
    logger.info(log_message)
