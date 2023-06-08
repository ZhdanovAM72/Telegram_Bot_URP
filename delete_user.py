import sqlite3

import logging
from logging.handlers import RotatingFileHandler


LOG_FILE = 'bot_log'


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


def delete_user():
    """Записываем данные пользователя по валидному коду."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            DELETE FROM bot_users
            WHERE id=7;
        """)
        # data = (id)
        cur.execute(sql_update_v1)
        con.commit()
        cur.close()
        logger.info('удален пользователь в БД: '
                    f'{id}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')

# user_id = 7

delete_user()
