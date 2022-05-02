from emoji import EMOJI_DATA


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
    new_chat_name = new_chat_name.replace(' ', '_')

    return new_chat_name
