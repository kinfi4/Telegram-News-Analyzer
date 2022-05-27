import os
import csv
from glob import glob
from datetime import datetime

import pandas as pd
from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel

import config.config as conf
from config.constants import NewsType
from services.utils import cut_channel_link, export_post_to_csv, get_or_create_channel_file
from services.config_reader import ConfigReader
from services.domain.text_preprocessor import TextPreprocessor
from services.domain.predictor import Predictor


client = TelegramClient('session-1', api_id=conf.API_ID, api_hash=conf.API_HASH)


def fetch_and_preprocess_news():
    with client:
        client.loop.run_until_complete(collect_posts())


async def collect_posts():
    channels_to_export_raw = conf.CHANNEL_REGISTRY['CHANNEL_LIST']
    channels_to_export_cut = map(cut_channel_link, channels_to_export_raw)

    conf_reader = ConfigReader('./config/.config')
    last_post_to_fetch_date = datetime.strptime(conf_reader.get(conf.LAST_POST_PUBLISH_DATE), conf.DATE_FORMAT)

    offset_date_string = conf_reader.get(conf.FIRST_POST_PUBLISH_DATE)
    offset_date = datetime.strptime(offset_date_string, conf.DATE_FORMAT) if offset_date_string else datetime.now().astimezone(tz=conf.LOCAL_TIMEZONE)

    last_post_parsed_date = offset_date

    processor = TextPreprocessor()

    try:
        for channel_name in channels_to_export_cut:
            print(f'Starting collecting data from {channel_name}: ')

            entity: Channel = await client.get_entity(channel_name)

            with get_or_create_channel_file(channel_name) as destination_file_obj:
                csv_writer = csv.writer(destination_file_obj)

                message: Message
                async for message in client.iter_messages(entity, limit=conf.MESSAGES_MAX_NUMBER_LIMIT, offset_date=offset_date):
                    if not message.text or len(message.text) < 20:
                        continue

                    post_date = message.date.astimezone(tz=conf.LOCAL_TIMEZONE)

                    if post_date < last_post_parsed_date:
                        last_post_parsed_date = post_date

                    if last_post_to_fetch_date and post_date < last_post_to_fetch_date:
                        break

                    export_post_to_csv(csv_writer, processor, message, post_date.date())

    finally:
        conf_reader.set(conf.FIRST_POST_PUBLISH_DATE, last_post_parsed_date.strftime(conf.DATE_FORMAT))


def classify_news():
    predictor = Predictor.create_from_files(
        conf.SENTIMENT_DICTIONARY_PATH,
        conf.SKLEARN_VECTORIZER,
        conf.KERAS_TOKENIZER,
        conf.KNN_MODEL_PATH,
        conf.SVC_MODEL_PATH,
        conf.DECISION_TREE_MODEL_PATH,
        conf.GAUSSIAN_MODEL_PATH,
        conf.LSTM_MODEL_PATH,
        conf.CNN_MODEL_PATH
    )

    destination_file_path = os.path.join(conf.CLASSIFIED_NEWS_FILE)
    with open(destination_file_path, 'w') as destination_file:
        csv_writer = csv.writer(destination_file)
        csv_writer.writerow(['channel_name', 'text', 'date', 'news_type', 'sentiment_type'])

        news_file_paths = glob(os.path.join(conf.NEWS_DATA_FOLDER_PATH, '*.csv'))

        for filepath in news_file_paths:
            filename = filepath.split('/')[-1]
            print(f'Start classification for file: {filename}...')

            with open(filepath) as source_csv_file:
                csv_reader = csv.reader(source_csv_file)

                # 0 - channel name, 1 - post text, 2 - post date
                for line in csv_reader:
                    channel_name, post_text, post_date = line

                    news_type = predictor.get_news_type(text=post_text)
                    sentiment_type = predictor.get_sentiment_type(text=post_text, news_type=news_type)

                    csv_writer.writerow([
                        channel_name,
                        post_text,
                        post_date,
                        news_type.value,
                        sentiment_type,
                    ])


def stack_shelling_words():
    print(f'Start stacking words from category: shelling')

    df = pd.read_csv(conf.CLASSIFIED_NEWS_FILE)

    df = df[df['news_type'] == NewsType.SHELLING.value]
    df = df['text'].str.split()
    df = df.apply(pd.Series).stack().reset_index(drop=True)

    df.to_csv(os.path.join(conf.PROCESSED_DATA_FOLDER_PATH, 'shelling-words.csv'), index=False)
