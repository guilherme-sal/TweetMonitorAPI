import sqlite3
from time import sleep
from apienviron.sql_environ import *


def connection_sqlite():

    conn = sqlite3.connect(PATH)
    return conn


def create_db():

    try:
        print(f'Creating db: {PATH}')

        with open(PATH, 'w'):
            pass
    except Exception as e:
        print(e)
        exit()


def create_target_table():

    print(f'Creating {TARGET_ACCOUNTS_TABLE_NAME}')
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE {TARGET_ACCOUNTS_TABLE_NAME}(
                TARGET_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                TARGET_NAME TEXT NOT NULL
        );
        """)
        conn.close()

    except Exception as e:
        print(e)
        exit()


def create_tweets_table():

    print(f'Creating {TWEETS_TABLE_NAME}')
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE {TWEETS_TABLE_NAME}(
                id INTEGER,
                conversation_id TEXT,
                created_at TEXT,
                date TEXT,
                timezone TEXT,
                place TEXT,
                tweet TEXT,
                language TEXT,
                hashtags TEXT,
                cashtags TEXT,
                user_id TEXT,
                user_id_str TEXT,
                username TEXT,
                name TEXT,
                day TEXT,
                hour TEXT,
                link TEXT,
                urls TEXT,
                photos TEXT,
                video TEXT,
                thumbnail TEXT,
                retweet TEXT,
                nlikes INTEGER,
                nreplies INTEGER,
                nretweets INTEGER,
                quote_url TEXT,
                search TEXT,
                near TEXT,
                geo TEXT,
                source TEXT,
                user_rt_id TEXT,
                user_rt TEXT,
                retweet_id TEXT,
                reply_to TEXT,
                retweet_date TEXT,
                translate TEXT,
                trans_src TEXT,
                trans_dest TEXT
        );
        """)
        conn.close()

    except Exception as e:
        print(e)
        exit()


if __name__ == '__main__':
    create_db()
    print('Db created with success')
    sleep(5)
    create_target_table()
    create_tweets_table()
    print('Tables created with success')
    print('Done!')