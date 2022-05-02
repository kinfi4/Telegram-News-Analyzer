import re
from string import punctuation

from nltk.tokenize import word_tokenize

from config.constants import Languages, emoji_regex_compiled
from config.config import RUSSIAN_STOP_WORDS, UKRAINIAN_STOP_WORDS


class TextPreprocessor:
    _ukrainian_letters = ('ї', 'і', 'є', 'ґ')
    _russian_letters = ('ы', 'э', 'ё', 'ъ')

    def __init__(self, text: str):
        self._text = text.lower()
        self.language = self._define_language()

    def make_preprocessing(self):
        self.remove_links()
        self.remove_emoji()
        self.remove_punctuation()
        self.remove_stop_words()
        self.remove_extra_spaces()

    def remove_links(self):
        self._text = re.sub(r'https?://\S+|www\.\S+', '', self._text)

    def remove_emoji(self):
        self._text = re.sub(emoji_regex_compiled, '', self._text)

    def remove_stop_words(self):
        stop_words = RUSSIAN_STOP_WORDS if self.language == Languages.RUSSIAN else UKRAINIAN_STOP_WORDS
        self._text = ' '.join([word for word in word_tokenize(self._text) if word not in stop_words])

    def remove_punctuation(self):
        self._text = re.sub(rf'[{punctuation}]', '', self._text)
        self._text = self._text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        self._text = self._text.replace('»', '').replace('«', '')

    def remove_extra_spaces(self):
        self._text = re.sub(' +', ' ', self._text)

    def get_text(self):
        return self._text

    def _define_language(self):
        if any([letter in self._text for letter in self._ukrainian_letters]):
            return Languages.UKRAINIAN
        else:
            return Languages.RUSSIAN
