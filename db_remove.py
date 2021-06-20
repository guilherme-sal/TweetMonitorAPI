import sqlite3
from apienviron.sql_environ import *

def connection_sqlite():

    conn = sqlite3.connect(PATH)
    return conn


def drop_target_table():

    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DROP TABLE {TARGET_ACCOUNTS_TABLE_NAME};
        """)
        conn.close()
    except Exception as e:
        print(e)
        pass


def drop_tweets_table():

    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DROP TABLE {TWEETS_TABLE_NAME};
        """)
        conn.close()
    except Exception as e:
        print(e)
        pass


def remove_db():

    global PATH

    try:
        os.remove(os.path.join(PATH))
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    drop_target_table()
    drop_tweets_table()
    remove_db()
