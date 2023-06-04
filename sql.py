import datetime as dt
import sqlite3

con = sqlite3.connect('users_v2.sqlite')
cur = con.cursor()

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
#     auth_code TEXT UNIQUE,
#     user_id INTEGER UNIQUE,
#     username TEXT,
#     first_name TEXT,
#     last_name TEXT,
#     register_date DATE
# );
# ''')

sql = "DELETE FROM bot_users WHERE id = 2"

cur.execute(sql)

# cur.execute('''
# DELETE FROM bot_users(
#     WHERE id = 1;
# );
# ''')

# bot_users = [
#     (1, 'admin-3javu0$%Q&k', 404025183, 'filmmaker89', 'Александр', 'Жданов', dt.datetime.now())
# ]


# cur.executemany('INSERT INTO bot_users VALUES(?, ?, ?, ?, ?, ?, ?);', bot_users)

con.commit()

con.close()
