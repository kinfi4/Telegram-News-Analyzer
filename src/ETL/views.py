from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel

import config.config as conf
from utils import cut_channel_link
from preprocessors import TextPreprocessor


client = TelegramClient('session-1', api_id=conf.API_ID, api_hash=conf.API_HASH)


async def collect_posts():
    channels_to_export_raw = conf.CHANNEL_REGISTRY['CHANNEL_LIST']
    channels_to_export_cut = map(cut_channel_link, channels_to_export_raw)

    for channel_name in channels_to_export_cut:
        entity: Channel = await client.get_entity(channel_name)

        message: Message
        async for message in client.iter_messages(entity, limit=conf.MESSAGES_MAX_NUMBER_LIMIT):
            if len(message.text) < 30:
                continue

            print(entity.title)
            print(message.date)

            text_preprocessor = TextPreprocessor(message.text)
            text_preprocessor.make_preprocessing()

            print(text_preprocessor.get_text())

            print('-' * 30)
