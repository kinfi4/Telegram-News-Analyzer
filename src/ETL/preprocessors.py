import re

from config.constants import Languages


class TextProcessor:
    ukrainian_letters = ('ї', 'і', 'є', 'ґ')
    russian_letters = ('ы', 'э', 'ё', 'ъ')

    def __init__(self, text: str):
        self.text = text
        self.language = self._define_language()

    def remove_links(self):
        self.text = re.sub(r'https?://\S+', '', self.text)

    def remove_emoji(self):
        pass

    def remove_stop_words(self):
        pass

    def tokenize(self):
        pass

    def _define_language(self):
        if any([letter in self.text for letter in self.ukrainian_letters]):
            return Languages.UKRAINIAN
        else:
            return Languages.RUSSIAN
