import os
import typing
from datetime import datetime

from emoji import EMOJI_DATA
from googletrans import Translator
from telethon.tl.custom.message import Message

from services.text_preprocessor import TextPreprocessor
from config.config import DATE_FORMAT, NEWS_DATA_FOLDER_PATH


def cut_channel_link(channel_link: str) -> str:
    """
        This function takes channel link in full format (https://t.me/<channel_name>) and
        returns it's short form: <channel_name>
    """
    return channel_link.split('/')[-1] if channel_link.startswith('https://t.me') else channel_link


def chat_name_standardizer(chat_name: str) -> str:
    """
        This function gets chat_name in a raw format, and removes all the spaces, invalid characters and so on

        Example: 24/7 - Новини України🇺🇦 -> 24/7_Новини_України
    """
    symbols_to_remove = ('|', '"', '\'', '-', ',', '.')
    new_chat_name = chat_name.translate({ord(c): '' for c in symbols_to_remove})
    new_chat_name = ''.join([c for c in new_chat_name if c not in EMOJI_DATA and ord(c) < 1200])
    new_chat_name = new_chat_name.strip()
    new_chat_name = new_chat_name.replace(' ', '_')

    return new_chat_name


def export_post_to_csv(csv_writer, translator: Translator, message: Message, post_date: datetime):
    channel_name = message.chat.title

    channel_name_preprocessor = TextPreprocessor(channel_name, translator)
    channel_name_preprocessor.remove_emoji()

    channel_name = channel_name_preprocessor.get_text()

    text_preprocessor = TextPreprocessor(message.text, translator=translator)
    text_preprocessor.make_all_preprocessing()

    preprocessed_text = text_preprocessor.get_text()

    csv_writer.writerow([
        channel_name,
        preprocessed_text,
        post_date.strftime(DATE_FORMAT),
        text_preprocessor.get_language().value
    ])


def get_or_create_channel_file(channel_cut_name: str) -> typing.TextIO:
    file_path = os.path.join(NEWS_DATA_FOLDER_PATH, channel_cut_name + '.csv')

    if os.path.exists(file_path):
        return open(file_path, 'a')

    return open(file_path, 'w')
