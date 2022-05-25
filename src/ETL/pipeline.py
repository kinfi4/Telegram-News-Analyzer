import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # we need this, in order not to print tensorflow warnings

from views import collect_posts, client
from services.domain.sentiment import SentimentAnalyzer


def fetch_and_preprocess_news():
    with client:
        client.loop.run_until_complete(collect_posts())


if __name__ == '__main__':
    # fetch_and_preprocess_news()
    sentiment = SentimentAnalyzer('/home/kinfi4/python/Propaganda-Analyzer/src/ETL/config/sentiment-words.csv')

    value = sentiment.define_sentiment_type('ира я тебе очень люблю')
    print(value)