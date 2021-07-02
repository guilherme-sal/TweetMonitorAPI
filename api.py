from datetime import datetime
import os
from flask import Flask
from flask_restful import Resource, Api
from apicore.cruds.target_table import return_target_info, create_target, return_targets_list, \
    delete_target_from_target_list
from apicore.functions import filter_unused_columns, format_alltweets_db_as_aggregated_info_df, format_target_string, \
    drop_duplicates_from_df
from apicore.cruds.tweets_table import return_tweets_table_as_df, return_tweets_from_target_as_list, \
    delete_tweets_from_target

app = Flask(__name__)
api = Api(app)


### LOG ENDPOINT ###
class Log(Resource):

    def get(self):
        try:
            log_lines = []
            with open('collect_engine/engine_log.txt', 'r') as logs:
                log = logs.readlines()
            for line in log:
                log_lines.append(line)
            return {'Code': 200, 'Alert': 'Sucess - Log returned.', 'Log': log_lines[-1]}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Log': None}


### COLLECT NOW ENDPOINT ###
class CollectNow(Resource):

    def get(self):
        try:
            os.system('python collect_engine/engine.py')
            return {'Code': 200, 'Alert': f'Success - Collect engine started at {datetime.now()}.'}
        except Exception as e:
            print(e)
            return {'Code': 400, 'Alert': 'Error - Collect engine failed!'}

### TARGET ENDPOINTS ###
class Target(Resource):

    def get(self, target):
        try:
            info = return_target_info(target)
            return {'Code': 200, 'Alert': 'Sucess - Target info retrieved.', 'Info': info}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Info': None}

    def post(self, target):
        target_list = return_targets_list()
        if target in target_list:
            return {'Code': 400, 'Alert': f'Error - Target {target} already on list!'}
        else:
            try:
                create_target(target)
                return {'Code': 200, 'Alert': f'Success - Target {target} added to list.'}
            except Exception as e:
                return {'Code': 400, 'Alert': f'Error - {e}.'}

    def delete(self, target):
        target_list = return_targets_list()
        if target in target_list:
            delete_target = delete_target_from_target_list(target)
            delete_tweets = delete_tweets_from_target(target)
            if delete_tweets and delete_target:
                return {'Code': 200, 'Alert': f'Success - Target {target} removed from list!'}
            else:
                return {'Code': 400, 'Alert': f'Error - Some error occurred during removal.'}

        else:
            return {'Code': 400, 'Alert': f'Error - Target {target} not found in target list!'}


class AllTargets(Resource):

    def get(self):
        try:
            target_list = return_targets_list()
            return {'Code': 200, 'Alert': 'Success - Target list retrieved.', 'Targets': target_list}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Targets': None}



### TWEETS ENDPOINT ###
class AllTweets(Resource):

    def get(self):
        try:
            df = return_tweets_table_as_df()
            df = filter_unused_columns(df)
            df = drop_duplicates_from_df(df)
            return {'Code': 200, 'Alert': 'Success - Dataframe retrieved.', 'Dataframe': df.to_dict('index')}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Dataframe': None}


class TweetsFromTarget(Resource):

    def get(self, target):
        try:
            target_df = return_tweets_from_target_as_list(target)
            target_df = filter_unused_columns(target_df)
            target_df = drop_duplicates_from_df(target_df)
            return {'Code': 200, 'Alert': 'Success - Dataframe retrieved.', 'Dataframe': target_df.to_dict('index')}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Dataframe': None}


### AGGREGATED ALLTWEETS DB ####

class AggregatedDB(Resource):

    def get(self):
        try:
            df = return_tweets_table_as_df()
            df = filter_unused_columns(df)
            df = drop_duplicates_from_df(df)
            df = format_alltweets_db_as_aggregated_info_df(df)
            return {'Code': 200, 'Alert': 'Success - Dataframe retrieved.', 'Dataframe': df.to_dict('index')}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}.', 'Dataframe': None}


### CREATE TARGETS FROM LIST ENDPOINT ###

class PostMultipleTargets(Resource):

    def post(self, t_list):
        try:
            t_list = t_list.strip().split(',')
            target_list = return_targets_list()
            targets_to_add = []

            for target in t_list:
                target = target.replace(",", '')
                target = format_target_string(target)
                if target in target_list:
                    pass
                else:
                    targets_to_add.append(target.strip())

            if targets_to_add:
                for target in targets_to_add:
                    create_target(target)
                return {'Code': 200, 'Alert': 'Success - Targets added to list', 'Targets added': targets_to_add}
            else:
                return {'Code': 400, 'Alert': 'Error - No new targets to add', 'Targets added': targets_to_add}
        except Exception as e:
            return {'Code': 400, 'Alert': f'Error - {e}', 'Targets added': None}




api.add_resource(Log, '/log')
api.add_resource(CollectNow, '/collectnow')
api.add_resource(Target, '/target/<string:target>')
api.add_resource(AllTargets, '/targets')
api.add_resource(AllTweets, '/tweets')
api.add_resource(TweetsFromTarget, '/tweets/<string:target>')
api.add_resource(AggregatedDB, '/tweets/aggregate/all')
api.add_resource(PostMultipleTargets, '/targets/postlist/<string:t_list>')


if __name__ == '__main__':
    app.run(debug=True)
