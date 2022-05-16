import re
from string import punctuation

from pymorphy2 import MorphAnalyzer
from nltk.tokenize import word_tokenize

from config.constants import emoji_regex_compiled
from config.config import RUSSIAN_STOP_WORDS


class TextPreprocessor:
    def __init__(self, morph: MorphAnalyzer = None):
        self._morph = morph if morph else MorphAnalyzer()

    def make_all_preprocessing(self, text: str) -> str:
        text = text.lower()
        text = self.remove_links(text)
        text = self.remove_emoji(text)
        text = self.remove_punctuation(text)
        text = self.remove_stop_words(text)
        text = self.remove_extra_spaces(text)

        return text

    def preprocess_and_lemmatize(self, text: str) -> str:
        text = self.make_all_preprocessing(text)
        tokens = word_tokenize(text, language='russian')

        return ' '.join((self._morph.parse(word)[0].normal_form for word in tokens))

    @staticmethod
    def remove_links(text: str):
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    @staticmethod
    def remove_emoji(text: str):
        return re.sub(emoji_regex_compiled, '', text)

    @staticmethod
    def remove_stop_words(text: str):
        return ' '.join([word for word in word_tokenize(text) if word not in RUSSIAN_STOP_WORDS])

    @staticmethod
    def remove_punctuation(text: str):
        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        return text.replace('»', '').replace('«', '')

    @staticmethod
    def remove_extra_spaces(text: str):
        return re.sub(' +', ' ', text)
