import os

# DATABASE ENNVIRONMENT
DB = 'database.sqlite3'
PATH = str(os.path.abspath(DB).split('TweetMonitorAPI')[0]) + f'TweetMonitorAPI/{DB}'
TARGET_ACCOUNTS_TABLE_NAME = 'target_table'
TWEETS_TABLE_NAME = 'tweets_table'

if __name__ == '__main__':
    print(PATH)