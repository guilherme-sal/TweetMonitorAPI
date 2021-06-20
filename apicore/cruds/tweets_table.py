from db_init import connection_sqlite
from apienviron.sql_environ import *
import pandas as pd


### CREATE
def create_rows(row):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
                INSERT INTO {TWEETS_TABLE_NAME} (id, conversation_id, created_at, date, timezone, place, tweet,
            language, hashtags, cashtags, user_id, user_id_str, username, name, day, hour, link, urls, photos, video,
            thumbnail, retweet, nlikes, nreplies, nretweets, quote_url, search, near, geo, source, user_rt_id, user_rt,
            retweet_id, reply_to, retweet_date, translate, trans_src, trans_dest)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], str(row[8]), str(row[9]), row[10], row[11],
        row[12], row[13],
        row[14], row[15], row[16], str(row[17]), str(row[18]), row[19], row[20], row[21], row[22], row[23], row[24],
        row[25],
        row[26], row[27], row[28], str(row[29]), row[30], row[31], row[32], row[33], str(row[34]), row[35], row[36],
        row[37]))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


### READ ###
def return_tweets_table_as_df():
    conn = connection_sqlite()
    df = pd.read_sql(f"SELECT * FROM {TWEETS_TABLE_NAME}", conn)
    return df


def return_tweets_table_targets_as_list():
    conn = connection_sqlite()
    df = pd.read_sql(f"SELECT * FROM {TWEETS_TABLE_NAME}", conn)
    target_list = [target for target in list(df['username'])]
    return target_list


def return_last_tweet_date__from_target(target):
    dates = []
    target = [target]
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT date FROM {TWEETS_TABLE_NAME}
            WHERE username = ?
            """, target)
    for date in cursor:
        dates.append(date[0])

    last_date = max(dates)
    return last_date


def return_tweets_from_target_as_list(target):
    df = return_tweets_table_as_df()
    df = df.query(f"username == '{target}'")
    return df


### Delete ###
def delete_tweets_from_target(target):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DELETE FROM {TWEETS_TABLE_NAME}
        WHERE username = ?
        """, (target,))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False

