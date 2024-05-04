import sqlite3

from bot.logger_setting.logger_bot import logger


class CheckPermissionsMethods:

    @classmethod
    def get_admin_access(cls, user_id: int) -> tuple:
        """"Проверяем данные администратора в БД."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT auth_code, user_id
                FROM bot_users
                WHERE user_id=? AND auth_code LIKE 'admin%'
                """,
                (user_id,)
            )
            admin_check = cursor.fetchone()
            cursor.close()
            logger.info(
                f'проверка прав администратора - '
                f'id пользователя: {user_id} - '
            )
            return admin_check

    @classmethod
    def get_moderator_access(cls, user_id: int) -> tuple:
        """"Проверяем данные модератора в БД."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT auth_code, user_id
                FROM bot_users
                WHERE user_id=? AND auth_code LIKE 'moderator%'
                """,
                (user_id,)
            )
            moderator_check = cursor.fetchone()
            cursor.close()
            logger.info(
                f'проверка прав модератора - '
                f'id пользователя: {user_id} - '
            )
            return moderator_check

    @classmethod
    def get_user_access(cls, user_id):
        """Проверяем пользователя в БД."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            user_check_in_db = (
                'SELECT id, user_id FROM bot_users WHERE user_id=?'
            )
            cursor.execute(user_check_in_db, (user_id,))
            user_check = cursor.fetchone()
            cursor.close()
            return user_check
