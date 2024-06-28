from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from bot.db.postgers_settings import PostgresSettings
from bot.logger_setting.logger_bot import logger


class Database:
    def __init__(self, settings: PostgresSettings) -> None:
        self.engine = create_engine(settings.postgres_connection_url, echo=True)
        self.SessionFactory = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))

    @contextmanager
    def get_session(self, old_session: Session = None) -> Session:
        session = old_session or self.SessionFactory()
        try:
            yield session
            if not old_session:
                session.commit()
        except Exception as e:
            logger.exception("Session rollback because of exception", exc_info=e)
            session.rollback()
            raise
        finally:
            if not old_session:
                session.close()
