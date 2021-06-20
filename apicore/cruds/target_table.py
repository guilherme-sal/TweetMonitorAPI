from db_init import connection_sqlite
from apienviron.sql_environ import *
import pandas as pd


### CREATE ###
def create_target(target):
    target = [target]
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {TARGET_ACCOUNTS_TABLE_NAME} (TARGET_NAME)
                VALUES (?)
                """, (target))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        pass


### READ ###
def return_target_info(target):
    info = []
    target = [target]
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT * FROM {TARGET_ACCOUNTS_TABLE_NAME}
            WHERE TARGET_NAME = ?
            """, target)
    for date in cursor:
        info.append(date[0])

    return info


def read_target_table_as_df():
    conn = connection_sqlite()
    df_target = pd.read_sql(f"SELECT * FROM {TARGET_ACCOUNTS_TABLE_NAME}", conn)
    return df_target


def return_targets_list():
    target_list = []
    conn = connection_sqlite()
    cursor = conn.cursor()
    cursor.execute(f"""
                    SELECT TARGET_NAME FROM {TARGET_ACCOUNTS_TABLE_NAME}
                    """, )
    for user_name in cursor:
        target_list.append(user_name[0])
    conn.close()
    return target_list


### DELETE
def delete_target_from_target_list(target):
    try:
        conn = connection_sqlite()
        cursor = conn.cursor()
        cursor.execute(f"""
        DELETE FROM {TARGET_ACCOUNTS_TABLE_NAME}
        WHERE TARGET_NAME = ?
        """, (target,))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    pass