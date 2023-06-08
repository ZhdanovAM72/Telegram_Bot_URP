import datetime as dt
import logging
import sqlite3
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


def get_new_code(code):
    """Записываем новый код в БД."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        bot_users = [
            (
             None,
             code,
             None,
             None,
             None,
             None,
             None,
            )
        ]
        cur.executemany(
            """
            INSERT OR IGNORE INTO bot_users
            VALUES(?, ?, ?, ?, ?, ?, ?);
            """,
            bot_users
        )
        con.commit()
        logger.info(f'Записан новый код в БД: {code}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')


def get_new_user(code: str, username, user_id, first_name, last_name):
    """Записываем данные пользователя по валидному коду."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            UPDATE bot_users
            SET user_id = ?,
            username = ?,
            first_name = ?,
            last_name = ?,
            register_date = ?
            WHERE auth_code = ? AND user_id IS NULL
        """)
        update_time = dt.datetime.now()
        data = (user_id, username, first_name, last_name, update_time, code)
        cur.execute(sql_update_v1, data)
        con.commit()
        cur.close()
        logger.info('Записан новый пользователь в БД: '
                    f'{user_id, first_name, last_name}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')
