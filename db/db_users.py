import datetime as dt
import sqlite3

from logger_setting.logger_bot import logger


def get_new_code(code: str):
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


def get_new_user(code: str, username: str, user_id: int, first_name: str, last_name: str) -> None:
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
        logger.info('Записан новый пользователь в БД: '
                    f'{user_id, first_name, last_name}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')


def create_new_moderator(code: str, user_id: int) -> None:
    """Дополняем пользователя правами модератора."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            UPDATE bot_users
            SET auth_code = ?
            WHERE user_id = ?
        """)
        data = (code, user_id)
        cur.execute(sql_update_v1, data)
        con.commit()
        logger.info('Записан новый модератор в БД: '
                    f'{user_id}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')


def update_user_code(old_code: str, new_code: int) -> None:
    """Обновляем код в БД."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            UPDATE bot_users
            SET auth_code = ?
            WHERE auth_code = ?
        """)
        data = (new_code, old_code)
        cur.execute(sql_update_v1, data)
        con.commit()
        logger.info('Записан новый код в БД: '
                    f'{new_code}')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')
