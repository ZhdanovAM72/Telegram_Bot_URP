import datetime as dt

from sqlalchemy import select
from sqlalchemy.orm import Session
from telebot.types import Message

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class CreateMethods:
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def create_new_email(cls, email: str, full_name: str, session: Session = None) -> None:
        try:
            with cls.db.get_session(session) as session:
                user = User(email=email, full_name=full_name)
                session.add(user)
                logger.info(f"Создан новый пользователь с email: {email, full_name}")
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя с email: {email, full_name} - {e}")

    @classmethod
    def user_sign_up(cls, email: str, tab_number: int, message: Message, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                user_query = session.execute(select(User).where(User.email == email))
                user = user_query.scalars().first()
                user.tab_namber = tab_number
                user.telegram_id = message.chat.id
                user.first_name = message.chat.first_name
                user.last_name = message.chat.last_name
                user.username = message.chat.username
                user.updated_at = dt.datetime.fromtimestamp(message.date)
                logger.info(f"Зарегистрирован новый пользователь: {email, tab_number}")
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя с данными: {tab_number, message.chat.id, email} - {e}")
