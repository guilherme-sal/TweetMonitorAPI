import threading
from datetime import datetime
from apicore.cruds.target_table import return_targets_list
from apicore.cruds.tweets_table import return_tweets_table_targets_as_list, create_rows, \
    return_last_tweet_date__from_target
import twint
import pandas as pd

ALL_TARGETS = set(return_targets_list())
OLD_TARGETS = set(return_tweets_table_targets_as_list())
NEW_TARGETS = ALL_TARGETS.difference(OLD_TARGETS)

DF = pd.DataFrame()


def collect_new_targets():
    global DF
    global NEW_TARGETS

    target = NEW_TARGETS.pop(0)

    print(f'#### New target: {target} ###\n')

    # Configure
    c = twint.Config()
    c.Username = target
    c.Show_hashtags = True
    c.Retweets = True
    c.Filter_retweets = False
    c.Since = "2021-01-01"
    c.Store_csv = True
    c.Pandas = True

    # Run
    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df

    df = df.drop_duplicates(subset=['id'])
    df = df.sort_values('date', ascending=False)

    DF = pd.concat([DF, df], ignore_index=True)


def collect_old_targets():
    global DF
    global OLD_TARGETS

    target = OLD_TARGETS.pop(0)

    print(f'Collecting tweets from: {target}...')
    last_date = return_last_tweet_date__from_target(target)
    print(f'Last tweet date: {last_date} \n')

    # Configure
    c = twint.Config()
    c.Username = target
    c.Show_hashtags = True
    c.Retweets = True
    c.Filter_retweets = False
    c.Since = last_date
    c.Pandas = True

    # Run
    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df

    df = df.drop_duplicates(subset=['id'])
    df = df.sort_values('date', ascending=False)
    DF = pd.concat([DF, df], ignore_index=True)


if __name__ == '__main__':

    engine_start = datetime.now()

    NEW_TARGETS = list(NEW_TARGETS)
    OLD_TARGETS = list(OLD_TARGETS)

    print(f'News targets list: {NEW_TARGETS}')
    print(f'Old targets list: {OLD_TARGETS}')

    ### New targets
    while NEW_TARGETS:
        THREADS = []
        for i in range(10):
            t = threading.Thread(target=collect_new_targets)
            THREADS.append(t)

        for t in THREADS:
            t.start()

        for t in THREADS:
            t.join()

    ### Old targets
    while OLD_TARGETS:
        THREADS = []
        for i in range(10):
            t = threading.Thread(target=collect_old_targets)
            THREADS.append(t)

        for t in THREADS:
            t.start()

        for t in THREADS:
            t.join()

    ### Saving DF to SQL ###
    print(f"\n### Saving tweets in database...")
    DF = DF.astype(str)
    DF['id'] = DF['id'].astype(int)
    DF = DF.drop_duplicates(subset=['id'])

    row_data_list = []
    for index, row in DF.iterrows():
        row_data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22],
                    row[23], row[24], row[25], row[26], row[27], row[28], row[17], row[29], row[30], row[31], row[32],
                    row[33], row[34], row[35], row[36], row[37]]
        row_data_list.append(row_data)
    create_rows(row_data_list)

    engine_end = datetime.now()

    ### Saving engine log ###
    with open('collect_engine/engine_log.txt', 'a') as log:
        log.write(
            f'Engine started at: #{engine_start}; Engine stopped at: #{engine_end}; #{len(DF)} tweets collected\n')

    print('### END ###')
