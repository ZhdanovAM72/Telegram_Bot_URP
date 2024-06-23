from sqlalchemy import select, not_
from sqlalchemy.orm import Session

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
    def search_telegram_id_user(cls, telegram_id: int, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_query.scalars().first()
                if not user:
                    return False
                logger.info("FIND ID NUMBER IN DB")
                return user.telegram_id
        except Exception as e:
            logger.error(f"Ошибка при регистрации на занятый id №: {telegram_id} - {e}")

    @classmethod
    def search_email_user(cls, email: str, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if not user:
                    return False
                logger.info("FIND EMAIL IN DB")
                return user.telegram_id
        except Exception as e:
            logger.error(f"Ошибка поиска email: {email} - {e}")

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
    def search_full_name_if_email(cls, email: str, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if not user:
                    session.close()
                    return False
                logger.info("FIND full_name NUMBER IN DB")
                return user.full_name
        except Exception as e:
            logger.error(f"Ошибка поиска данных: {email} - {e}")

    @classmethod
    def search_all_users(cls, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user = session.query(User).filter(not_(User.telegram_id.is_(None))).all()
                logger.info(user)
                if not user:
                    session.close()
                    return False
                logger.info("FIND full_name NUMBER IN DB")
                return user
        except Exception as e:
            logger.error(f"Ошибка поиска данных: {e}")
