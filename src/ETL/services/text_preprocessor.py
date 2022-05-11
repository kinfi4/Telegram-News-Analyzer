import re
from string import punctuation

from nltk.tokenize import word_tokenize
from googletrans import Translator

from config.constants import Languages, emoji_regex_compiled
from config.config import RUSSIAN_STOP_WORDS, UKRAINIAN_STOP_WORDS


class TextPreprocessor:
    def __init__(self, text: str, translator: Translator):
        self._text = text.lower()
        self._translator = translator
        self._language = None

    def make_all_preprocessing(self):
        self._language = self.define_language()

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
        stop_words = RUSSIAN_STOP_WORDS if self._language == Languages.RUSSIAN else UKRAINIAN_STOP_WORDS
        self._text = ' '.join([word for word in word_tokenize(self._text) if word not in stop_words])

    def remove_punctuation(self):
        self._text = re.sub(rf'[{punctuation}]', '', self._text)
        self._text = self._text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        self._text = self._text.replace('»', '').replace('«', '')

    def remove_extra_spaces(self):
        self._text = re.sub(' +', ' ', self._text)

    def get_text(self):
        return self._text

    def get_language(self):
        return self._language

    def define_language(self):
        return Languages.RUSSIAN if self._translator.detect(self._text).lang == 'ru' else Languages.UKRAINIAN
