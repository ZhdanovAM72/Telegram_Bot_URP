import sqlite3

import pandas as pd

from logger_setting.logger_bot import logger


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
