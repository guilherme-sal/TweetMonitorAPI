

def format_target_string(target):
    target = target.strip()
    if target.startswith('@'):
        target = target[1:]
    return target


def filter_unused_columns(df):
    df = df[['id', 'username', 'date', 'tweet', 'nlikes', 'nretweets', 'nreplies', 'hashtags', 'urls', 'photos']]
    return df


def format_alltweets_db_as_aggregated_info_df(df):

    df['tweets'] = 1
    df_info = df[['username', 'date', 'tweets', 'nlikes', 'nreplies', 'nretweets']]

    last_tweet_list = []
    first_tweet_list = []
    for target in df_info['username'].unique():
        df_filtered = df_info.query(f'username == "{target}"')
        last_tweet = df_filtered['date'].max()
        first_tweet = df_filtered['date'].min()
        last_tweet_list.append(last_tweet)
        first_tweet_list.append(first_tweet)

    df_grouped = df_info.groupby('username').sum()
    df_grouped = df_grouped.astype(int)
    df_grouped['first_tweet'] = first_tweet_list
    df_grouped['last_tweet'] = last_tweet_list
    df_grouped = df_grouped.reset_index()
    return df_grouped