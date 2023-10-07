import sqlite3

con = sqlite3.connect('users_v2.sqlite')
cur = con.cursor()


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

con.commit()

con.close()
