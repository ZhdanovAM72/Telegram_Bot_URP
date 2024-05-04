import datetime as dt
import sqlite3

from bot.logger_setting.logger_bot import logger


class CreateMethods:

    @classmethod
    def create_new_code(cls, code: str) -> None:
        """Записываем новый код в БД."""
        try:
            con = sqlite3.connect('users_v2.sqlite')
            cur = con.cursor()
            bot_users = [
                (None, code, None, None, None, None, None)
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

    @classmethod
    def create_new_user(
            cls,
            code: str,
            username: str,
            user_id: int,
            first_name: str,
            last_name: str,
         ) -> None:
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
            data = (
                user_id, username, first_name, last_name, update_time, code
            )
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
