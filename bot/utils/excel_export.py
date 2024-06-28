from psycopg2 import Error
import pandas as pd
from sqlalchemy import create_engine, null, not_
from sqlalchemy.orm import Session

from bot.logger_setting.logger_bot import logger
from bot.db.database import Database, PostgresSettings
from bot.db.entities.users import User


class ExcelExport:
    """Класс для работы с Excel."""
    settings = PostgresSettings()
    db = Database(settings)

    @classmethod
    def excel_export_new(cls, session: Session = None):
        try:
            with cls.db.get_session(session) as session:
                users_count = session.query(User).where(not_(User.telegram_id == null())).count()
                accounts_count = session.query(User).where(not_(User.full_name == null())).count()
                engine = create_engine(cls.settings.postgres_connection_url)
                df = pd.read_sql_table('users', engine)
                if df.empty:
                    logger.info("No data to export.")
                    return None
                logger.info('Выгрузка БД в excel.')
                df.to_excel('result.xlsx', index=False)
                return accounts_count, users_count
        except Error as e:
            logger.error(f"Ошибка при подключении к БД: {e}")
        except Exception as e:
            logger.error(f"Ошибка при выгрузке данных в Excel: {e}")
