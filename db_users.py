import datetime as dt
import sqlite3
import os
import sqlite3
from random import choice
import logging
from logging.handlers import RotatingFileHandler

import telebot


def get_new_code(code):
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        bot_users = [
            (
             None,
             code,
             None,
             None,
             None,
             None,
             None,
            )
        ]
        cur.executemany(
            """
            INSERT OR IGNORE INTO bot_users
            VALUES(?, ?, ?, ?, ?, ?, ?);
            """,
            bot_users
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе с БД", error)
    finally:
        if con:
            con.close()
            print("Соединение с БД закрыто")


def get_new_user(code: str, username, user_id, first_name, last_name):
    try:
        con = sqlite3.connect('users_v2.sqlite')
        cur = con.cursor()
        sql_update_v1 = ("""
            UPDATE bot_users
            SET user_id = ?,
            username = ?,
            first_name = ?,
            last_name = ?,
            register_date = ?
            WHERE auth_code = ? AND user_id IS NULL
        """)
        update_time = dt.datetime.now()
        data = (user_id, username, first_name, last_name, update_time, code)
        cur.execute(sql_update_v1, data)
        con.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с БД", error)
    finally:
        if con:
            con.close()
            print("Соединение с БД закрыто")


# post_code: str = 'SOC0E1ZH?nOW+g-i'
#get_new_code(post_code)

# atr_2 = 'Alex'
# atr_3 = 33332245679
# atr_4 = 'ТЕСТфест'
# atr_5 = 'ТЕСТласт'

# get_new_user(post_code, atr_2, atr_3, atr_4, atr_5)

# cur.execute('''
# CREATE TABLE IF NOT EXISTS bot_users(
#     id INTEGER PRIMARY KEY,
#     code TEXT,
#     user_id INTEGER
# );
# ''')

# cur.execute('''
# CREATE TABLE IF NOT EXISTS bot_users(
#     id INTEGER PRIMARY KEY,
#     auth_code TEXT UNIQIE,
#     user_id INTEGER UNIQIE,
#     username TEXT,
#     first_name TEXT,
#     last_name TEXT,
#     register_date DATE
# );
# ''')


