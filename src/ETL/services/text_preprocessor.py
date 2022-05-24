import re
from string import punctuation

import numpy as np
import pandas as pd
from pymorphy2 import MorphAnalyzer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

from config.constants import emoji_regex_compiled
from config.config import RUSSIAN_STOP_WORDS, MAX_POST_LEN_IN_WORDS


class TextPreprocessor:
    def __init__(
            self,
            morph: MorphAnalyzer = None,
            sklearn_vectorizer: TfidfVectorizer = None,
            keras_tokenizer: Tokenizer = None
    ):
        self._morph = morph if morph else MorphAnalyzer()
        self._vectorizer = sklearn_vectorizer if sklearn_vectorizer else TfidfVectorizer()
        self._tokenizer = keras_tokenizer if keras_tokenizer else Tokenizer()

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

    def keras_tokenize_and_pad_text(
            self,
            texts: pd.Series,
            make_preprocessing: bool = True,
            max_words_number: int = MAX_POST_LEN_IN_WORDS,
            padding: str = 'pre',
            truncating: str = 'pre',
    ) -> np.ndarray:
        if make_preprocessing:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_and_lemmatize)

        tokens = self._tokenizer.texts_to_sequences(texts)
        padded_tokens = pad_sequences(tokens, maxlen=max_words_number, padding=padding, truncating=truncating)
        return np.array(padded_tokens)

    def sklearn_vectorize_text(self, texts: pd.Series, make_preprocessing: bool = True):
        if make_preprocessing:
            texts = texts if isinstance(texts, pd.Series) else pd.Series(texts)
            texts = texts.apply(self.preprocess_and_lemmatize)

        return self._vectorizer.transform(texts)

    @staticmethod
    def remove_links(text: str):
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    @staticmethod
    def remove_emoji(text: str):
        return re.sub(emoji_regex_compiled, '', text)

    @staticmethod
    def remove_stop_words(text: str):
        cleared_words = [word for word in word_tokenize(text) if word not in RUSSIAN_STOP_WORDS]
        truncated_text = cleared_words[:MAX_POST_LEN_IN_WORDS]
        return ' '.join(truncated_text)

    @staticmethod
    def remove_punctuation(text: str):
        text = re.sub(rf'[{punctuation}]', '', text)
        text = text.replace(' – ', ' ').replace(' - ', ' ').replace(' — ', ' ')
        return text.replace('»', '').replace('«', '')

    @staticmethod
    def remove_extra_spaces(text: str):
        return re.sub(' +', ' ', text)
