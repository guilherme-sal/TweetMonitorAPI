

def format_target_string(target):
    target = target.strip()
    if target.startswith('@'):
        target = target[1:]
    return target


def filter_unused_columns(df):
    df = df[['id', 'username', 'date', 'tweet', 'nlikes', 'nretweets', 'nreplies', 'hashtags', 'urls', 'photos',
             'thumbnail', 'language']]
    return df


def format_alltweets_db_as_aggregated_info_df(df):

    df['tweets'] = 1
    df_info = df[['username', 'date', 'tweets', 'nlikes', 'nreplies', 'nretweets']]

    df_grouped = df_info.groupby('username').sum()
    df_grouped = df_grouped.astype(int)
    df_grouped = df_grouped.reset_index()
    df_grouped = df_grouped.sort_values('username')

    last_tweet_list = []
    first_tweet_list = []
    for target in df_grouped['username'].unique():
        df_filtered = df_info.query(f'username == "{target}"')
        last_tweet = df_filtered['date'].max()
        first_tweet = df_filtered['date'].min()
        last_tweet_list.append(last_tweet)
        first_tweet_list.append(first_tweet)
    df_grouped['first_tweet'] = first_tweet_list
    df_grouped['last_tweet'] = last_tweet_list

    return df_grouped


def drop_duplicates_from_df(df):
    df = df.drop_duplicates(subset=['id'])
    return df
