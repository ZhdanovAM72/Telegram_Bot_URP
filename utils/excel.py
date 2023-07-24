import pandas as pd
import logging
import sqlite3
from logging.handlers import RotatingFileHandler


LOG_FILE = 'bot_log.txt'


def init_logger() -> logging.Logger:
    """Определяем настройки логгера."""
    logging.basicConfig(
        format=('%(asctime)s - %(levelname)s - %(name)s - '
                'строка: %(lineno)d - %(message)s'),
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=5_000_000,
                backupCount=5
            )
        ],
    )
    return logging.getLogger(__name__)


logger = init_logger()


def excel_export():
    """Выгрузка данных БД в excel."""
    try:
        con = sqlite3.connect('users_v2.sqlite')
        df = pd.read_sql('SELECT * FROM bot_users', con)
        df.to_excel('result.xlsx', index=False)
        logger.info('Выгрузка БД в excel.')
    except sqlite3.Error as error:
        logger.error(f'SQL error: {error}')
    finally:
        if con:
            con.close()
            logger.info('Закрыто соединение с БД: users_v2')
