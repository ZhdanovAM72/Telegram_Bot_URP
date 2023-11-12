import sqlite3


def search_user_id_in_db(chat_id):
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


def search_code_in_db(code):
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