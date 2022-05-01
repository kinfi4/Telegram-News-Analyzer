import json


API_ID = '10722341'
API_HASH = '35e06edc1b465131d9282ca13c5e64fe'
DATA_FOLDER_PATH = '/home/kinfi4/python/Propaganda-Analyzer/src/data'

MESSAGES_MAX_NUMBER_LIMIT = 5

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/CHANNEL_REGISTRY.json') as registry_file:
    CHANNEL_REGISTRY = json.load(registry_file)

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/UKRAINIAN_STOP_WORDS.json') as ukrainian_stop_words_file:
    UKRAINIAN_STOP_WORDS = json.load(ukrainian_stop_words_file)

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/RUSSIAN_STOP_WORDS.json') as russian_stop_words_file:
    RUSSIAN_STOP_WORDS = json.load(russian_stop_words_file)
