import sqlite3

from bot.logger_setting.logger_bot import logger


class DeleteMethods:

    @classmethod
    def delete_by_chat_id(cls, chat_id: int) -> None:
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

    @classmethod
    def delete_by_code(cls, auth_code: str) -> None:
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
