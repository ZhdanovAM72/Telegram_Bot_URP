import sqlite3

from bot.logger_setting.logger_bot import logger


class UpdateMethods:

    @classmethod
    def update_user_to_moderator(cls, code: str, user_id: int) -> None:
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

    @classmethod
    def update_user_code(cls, old_code: str, new_code: int) -> None:
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
