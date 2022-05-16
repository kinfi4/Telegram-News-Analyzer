import os
import json


API_ID = '17332691'
API_HASH = '626a6ab20ca7d1c151a4d1984448fd0c'
DATA_FOLDER_PATH = '/home/kinfi4/python/Propaganda-Analyzer/src/data'
NEWS_DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'news-posts')

LAST_POST_PUBLISH_DATE = 'LAST_POST_PUBLISH_DATE'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

MESSAGES_MAX_NUMBER_LIMIT = 2

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/CHANNEL_REGISTRY.json') as registry_file:
    CHANNEL_REGISTRY = json.load(registry_file)

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/RUSSIAN_STOP_WORDS.json') as russian_stop_words_file:
    RUSSIAN_STOP_WORDS = json.load(russian_stop_words_file)
