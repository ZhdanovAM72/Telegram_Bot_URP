import sqlite3


class SearchMethods:

    @classmethod
    def search_user_id_in_db(cls, chat_id):
        """Проверяем наличие user_id в БД."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            search_db_user = ('SELECT user_id, auth_code '
                              'FROM bot_users WHERE user_id=?')
            cursor.execute(
                search_db_user,
                (chat_id,)
            )
            search_user = cursor.fetchone()
            cursor.close()
            return search_user

    @classmethod
    def search_code_in_db(cls, code):
        """Проверяем наличие кода доступа в БД."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            search_db = ('SELECT auth_code, user_id '
                         'FROM bot_users WHERE auth_code=?')
            cursor.execute(
                search_db,
                (code,)
            )
            search_code = cursor.fetchone()
            cursor.close()
            return search_code

    @classmethod
    def search_all_user_id(cls):
        """Поиск всех пользователей в базе данных."""
        with sqlite3.connect('users_v2.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT user_id FROM bot_users WHERE user_id IS NOT NULL
                """
            )
            search_all_ids = cursor.fetchall()
            cursor.close()
            return search_all_ids
