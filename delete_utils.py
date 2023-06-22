import sqlite3

import logging
from logging.handlers import RotatingFileHandler


LOG_FILE = 'bot_log.txt'


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


def delete_user(chat_id):
    """Удаляем данные пользователя по user_id."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            DELETE FROM bot_users
            WHERE user_id = ?;
        """)
        cur.execute(sql_update_v1, (chat_id,))
        con.commit()
        cur.close()
        logger.info('Команда удаления пользователя в БД, id: '
                    f'{chat_id}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')


def delete_code(auth_code):
    """Удаляем все данные привязанные с auth_code."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            DELETE FROM bot_users
            WHERE auth_code = ?;
        """)
        cur.execute(sql_update_v1, (auth_code,))
        con.commit()
        cur.close()
        logger.info('Команда удаления дынных из БД по коду: '
                    f'{auth_code}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')
