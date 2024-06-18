import sqlite3

from sqlalchemy import select
from sqlalchemy.orm import Session
# from telebot.types import Message

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class SearchMethods:
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def search_email_in_db(cls, email: str, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if not user:
                    session.close()
                    logger.info("NOT EMAIL IN DB")
                    return None
                return True
        except Exception as e:
            logger.error(f"Ошибка при поиске email: {email} - {e}")

    @classmethod
    def search_tab_number_in_db(cls, tab_number: int, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.tab_namber == tab_number))
                user = user_query.scalars().first()
                if not user:
                    session.close()
                    return True
                logger.info("FIND TAB NUMBER IN DB")
                return None
        except Exception as e:
            logger.error(f"Ошибка при регистрации на занятый табельный №: {tab_number} - {e}")

    @classmethod
    def search_telegram_id_in_db(cls, telegram_id: int, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_query.scalars().first()
                if not user:
                    session.close()
                    return True
                logger.info("FIND ID NUMBER IN DB")
                return None
        except Exception as e:
            logger.error(f"Ошибка при регистрации на занятый id №: {telegram_id} - {e}")

    @classmethod
    def search_full_name_in_db(cls, telegram_id: int, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_query.scalars().first()
                if not user:
                    session.close()
                    return False
                logger.info("FIND ID NUMBER IN DB")
                return user.full_name
        except Exception as e:
            logger.error(f"Ошибка при регистрации на занятый id №: {telegram_id} - {e}")

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
