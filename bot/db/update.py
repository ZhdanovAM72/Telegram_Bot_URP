import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot.types import Message

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class UpdateMethods:
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def update_user_to_moderator(cls, telegram_id: int, message: Message, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_query.scalars().first()
                if not user:
                    return False
                user.is_moderator = True
                user.updated_at = dt.datetime.fromtimestamp(message.date)
                logger.info(f"Added new moderator: {user.telegram_id}")
                return user.telegram_id
        except Exception as e:
            logger.error(f"Ошибка назначения модератора id №: {telegram_id} - {e}")

    @classmethod
    def update_user_to_admin(cls, telegram_id: int, message: Message, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.telegram_id == telegram_id))
                user = user_query.scalars().first()
                if not user:
                    return False
                user.is_admin = True
                user.updated_at = dt.datetime.fromtimestamp(message.date)
                logger.info(f"Added new administrator: {user.telegram_id}")
                return user.telegram_id
        except Exception as e:
            logger.error(f"Ошибка назначения модератора id №: {telegram_id} - {e}")
