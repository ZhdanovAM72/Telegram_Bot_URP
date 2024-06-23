import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot.types import Message

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class DeleteMethods:
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def delete_email(cls, email: str, session: Session = None) -> bool:
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if user.email and not (user.is_admin or user.is_moderator):
                    logger.info(f"Удаление успешно! Пользователь: {email}")
                    session.delete(user)
                    session.commit()
                    return True
                logger.info(f"Удаление неуспешно! Пользователь: {email}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя с данными: {email} - {e}")

    @classmethod
    def delete_moderator_by_email(cls, email: str, message: Message, session: Session = None) -> bool:
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if user.is_moderator:
                    logger.info(f"Удаление прав успешно! Пользователь: {email}")
                    user.is_moderator = False
                    user.updated_at = dt.datetime.fromtimestamp(message.date)
                    session.commit()
                    return True
                logger.info(f"Удаление прав неуспешно! Пользователь: {email}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя с данными: {email} - {e}")

    @classmethod
    def delete_admin_by_email(cls, email: str, message: Message, session: Session = None) -> bool:
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                if user.is_admin:
                    logger.info(f"Удаление прав успешно! Пользователь: {email}")
                    user.is_admin = False
                    user.updated_at = dt.datetime.fromtimestamp(message.date)
                    session.commit()
                    return True
                logger.info(f"Удаление прав неуспешно! Пользователь: {email}")
                return False
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя с данными: {email} - {e}")
