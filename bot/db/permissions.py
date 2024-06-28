from sqlalchemy import select
from sqlalchemy.orm import Session

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class CheckPermissionsMethods:
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def get_admin_access(cls, user_id: int, session: Session = None) -> tuple:
        """"Проверяем данные администратора в БД."""
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == user_id))
                user = user_query.scalars().first()
                if user.is_admin:
                    return True
                logger.info(f"Проверка прав администратора неуспешна! Пользователь: {user_id}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя с данными: {user_id} - {e}")

    @classmethod
    def get_moderator_access(cls, user_id: int, session: Session = None) -> tuple:
        """"Проверяем данные модератора в БД."""
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == user_id))
                user = user_query.scalars().first()
                if user.is_moderator:
                    return True
                logger.info(f"Проверка прав модератора неуспешна! Пользователь: {user_id}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя с данными: {user_id} - {e}")

    @classmethod
    def get_user_access(cls, user_id: int, session: Session = None) -> tuple:
        """Проверяем пользователя в БД."""
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == user_id))
                user = user_query.scalars().first()
                if user.telegram_id:
                    return True
                logger.info(f"Проверка прав пользователя неуспешна! Пользователь: {user_id}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя с данными: {user_id} - {e}")
