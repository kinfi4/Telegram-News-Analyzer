import csv
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.custom.message import Message
from telethon.tl.types import Channel

import config.config as conf
from services.utils import cut_channel_link, export_post_to_csv, get_or_create_channel_file
from services.config_reader import ConfigReader
from services.text_preprocessor import TextPreprocessor


client = TelegramClient('session-1', api_id=conf.API_ID, api_hash=conf.API_HASH)


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
            entity: Channel = await client.get_entity(channel_name)

            with get_or_create_channel_file(channel_name) as destination_file_obj:
                csv_writer = csv.writer(destination_file_obj)

                message: Message
                async for message in client.iter_messages(entity, limit=conf.MESSAGES_MAX_NUMBER_LIMIT, offset_date=offset_date):
                    if not message.text or len(message.text) < 20:
                        continue

                    post_date = message.date.astimezone(tz=conf.LOCAL_TIMEZONE)

                    print(message.chat.title, post_date, last_post_parsed_date)

                    if post_date < last_post_parsed_date:
                        last_post_parsed_date = post_date

                    if last_post_to_fetch_date and post_date < last_post_to_fetch_date:
                        break

                    export_post_to_csv(csv_writer, processor, message, post_date)
    finally:
        conf_reader.set(conf.FIRST_POST_PUBLISH_DATE, last_post_parsed_date.strftime(conf.DATE_FORMAT))
