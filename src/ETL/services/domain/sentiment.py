import os
from typing import Optional
from abc import ABC, abstractmethod
from collections import namedtuple

from nltk.tokenize import word_tokenize

from config.constants import SentimentTypes, NewsType


Word = namedtuple('Word', 'form label value')


class CsvFileIndex:
    def __init__(self, filepath: str, delimiter: str = ',', skip_header: bool = True):
        with open(filepath) as csv_file:
            self._lines = csv_file.readlines()[1:] if skip_header else csv_file.readlines()

        self.words = [
            Word(
                form=line.split(delimiter)[0],
                label=line.split(delimiter)[1],
                value=float(line.split(delimiter)[2]),
            )
            for line in self._lines
        ]

    def find_word_binary(self, word: str) -> Optional[Word]:
        word_idx = self._binary_search(0, len(self.words) - 1, word)

        if word_idx is not None:
            return self.words[word_idx]

    def _binary_search(self, left_idx: int, right_idx: int, word: str) -> Optional[int]:
        if right_idx >= left_idx:
            average_idx = int(left_idx + (right_idx - left_idx) / 2)

            if self.words[average_idx].form == word:
                return average_idx
            elif self.words[average_idx].form < word:
                return self._binary_search(average_idx + 1, right_idx, word)
            else:
                return self._binary_search(left_idx, average_idx - 1, word)


class ISentimentAnalyzer(ABC):
    @abstractmethod
    def define_sentiment_type(self, text: str, text_type: NewsType) -> SentimentTypes:
        pass


class SentimentAnalyzer(ISentimentAnalyzer):
    _negative_marks = ('не',)
    _positive_level_threshold = 1
    _negative_level_threshold = -0.1
    _initial_sentiment_value = {
        NewsType.HUMANITARIAN: 0.2, NewsType.SHELLING: -1.1, NewsType.POLITICAL: -0.1, NewsType.ECONOMICAL: -0.2
    }

    def __init__(self, sentiment_dictionary_filepath: str):
        if not os.path.exists(sentiment_dictionary_filepath):
            raise AttributeError(f'Sentiment dictionary: {sentiment_dictionary_filepath} does not exist')

        self._word_indexator = CsvFileIndex(sentiment_dictionary_filepath, delimiter=',')

    def define_sentiment_type(self, text: str, text_type: NewsType) -> SentimentTypes:
        tokens = word_tokenize(text, language='russian')

        tokens_sentiment_values, negativation_coefficient = [], 1
        for token in tokens:
            if token in self._negative_marks:
                negativation_coefficient = -1
                continue

            tokens_sentiment_values.append(self._find_word_sentiment_value(token, coefficient=negativation_coefficient))
            negativation_coefficient = 1

        text_sentiment_value = self._initial_sentiment_value[text_type]
        text_sentiment_value += sum(tokens_sentiment_values)

        print(f'Text: {text} - {text_sentiment_value}', {sum(tokens_sentiment_values)})

        if text_sentiment_value > self._positive_level_threshold:
            return SentimentTypes.POSITIVE
        elif text_sentiment_value < self._negative_level_threshold:
            return SentimentTypes.NEGATIVE
        else:
            return SentimentTypes.NEUTRAL

    def _find_word_sentiment_value(self, word: str, coefficient: int = 1) -> float:
        word_obj = self._word_indexator.find_word_binary(word)

        if word_obj is None:
            return 0

        return word_obj.value * coefficient
