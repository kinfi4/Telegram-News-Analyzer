import datetime
import os
import json


API_ID = '17332691'
API_HASH = '626a6ab20ca7d1c151a4d1984448fd0c'

DATA_FOLDER_PATH = '/home/kinfi4/python/Propaganda-Analyzer/src/data'
NEWS_DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'news-posts')
PROCESSED_DATA_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, 'processed-data')

CLASSIFIED_NEWS_FILE = os.path.join(PROCESSED_DATA_FOLDER_PATH, 'classified-news.csv')

SENTIMENT_DICTIONARY_PATH = '/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/sentiment-words.csv'

TRAINED_MODELS_PATH = '/home/kinfi4/python/Propaganda-Analyzer/src/models/trained-models'

CNN_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'cnn-news-type-prediction.h5')
LSTM_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'lstm-news-type-prediction.h5')
SVC_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'svc-news-type-prediction.sav')
KNN_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'knn-news-type-prediction.sav')
GAUSSIAN_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'nb-news-type-prediction.sav')
DECISION_TREE_MODEL_PATH = os.path.join(TRAINED_MODELS_PATH, 'tree-news-type-prediction.sav')

SKLEARN_VECTORIZER = os.path.join(TRAINED_MODELS_PATH, 'vectorizer.pk')
KERAS_TOKENIZER = os.path.join(TRAINED_MODELS_PATH, 'keras-tokenizer.pk')


LAST_POST_PUBLISH_DATE = 'LAST_POST_PUBLISH_DATE'
FIRST_POST_PUBLISH_DATE = 'FIRST_POST_PUBLISH_DATE'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S%z'

# MESSAGES_MAX_NUMBER_LIMIT = 150
MESSAGES_MAX_NUMBER_LIMIT = 70_000

MAX_POST_LEN_IN_WORDS = 20
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/CHANNEL_REGISTRY.json') as registry_file:
    CHANNEL_REGISTRY = json.load(registry_file)

with open('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/RUSSIAN_STOP_WORDS.json') as russian_stop_words_file:
    RUSSIAN_STOP_WORDS = json.load(russian_stop_words_file)
