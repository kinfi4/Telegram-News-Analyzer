import csv
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel
from googletrans import Translator

import config.config as conf
from services.utils import cut_channel_link, export_post_to_csv, get_or_create_channel_file
from services.config_reader import ConfigReader


client = TelegramClient('session-1', api_id=conf.API_ID, api_hash=conf.API_HASH)


async def collect_posts():
    channels_to_export_raw = conf.CHANNEL_REGISTRY['CHANNEL_LIST'][:3]
    channels_to_export_cut = map(cut_channel_link, channels_to_export_raw)

    conf_reader = ConfigReader('./config/.config')
    last_post_to_fetch_date = datetime.strptime(conf_reader.get(conf.LAST_POST_PUBLISH_DATE), conf.DATE_FORMAT)

    translator = Translator()

    for channel_name in channels_to_export_cut:
        entity: Channel = await client.get_entity(channel_name)

        with get_or_create_channel_file(channel_name) as destination_file_obj:
            csv_writer = csv.writer(destination_file_obj)

            message: Message
            async for message in client.iter_messages(entity, limit=conf.MESSAGES_MAX_NUMBER_LIMIT):
                post_date = message.date.astimezone(last_post_to_fetch_date.tzinfo)
                print(entity.title, post_date, len(message.text))

                if len(message.text) < 20:
                    continue

                if last_post_to_fetch_date and post_date < last_post_to_fetch_date.astimezone(last_post_to_fetch_date.tzinfo):
                    break

                export_post_to_csv(csv_writer, translator, message, post_date)

    conf_reader.set(conf.LAST_POST_PUBLISH_DATE, datetime.now().strftime(conf.DATE_FORMAT))
