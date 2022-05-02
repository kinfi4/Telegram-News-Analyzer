from datetime import datetime

from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel

import config.config as conf
from services.utils import cut_channel_link
from services.text_preprocessor import TextPreprocessor
from services.config_reader import ConfigReader


client = TelegramClient('session-1', api_id=conf.API_ID, api_hash=conf.API_HASH)


async def collect_posts():
    channels_to_export_raw = conf.CHANNEL_REGISTRY['CHANNEL_LIST']
    channels_to_export_cut = map(cut_channel_link, channels_to_export_raw)

    conf_reader = ConfigReader('./config/.config')
    last_post_to_fetch_date = datetime.strptime(conf_reader.get(conf.LAST_POST_PUBLISH_DATE), conf.DATE_FORMAT)

    for channel_name in channels_to_export_cut:
        entity: Channel = await client.get_entity(channel_name)

        message: Message
        async for message in client.iter_messages(entity, limit=conf.MESSAGES_MAX_NUMBER_LIMIT):
            if len(message.text) < 20:
                continue

            post_date = message.date.astimezone(last_post_to_fetch_date.tzinfo)
            if last_post_to_fetch_date and post_date < last_post_to_fetch_date.astimezone(last_post_to_fetch_date.tzinfo):
                break

            print(entity.title)
            print(post_date)

            text_preprocessor = TextPreprocessor(message.text)
            text_preprocessor.make_preprocessing()

            print(text_preprocessor.get_text())

            print('-' * 30)

    conf_reader.set(conf.LAST_POST_PUBLISH_DATE, datetime.now().strftime(conf.DATE_FORMAT))
