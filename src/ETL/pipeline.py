import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # we need this, in order not to print tensorflow warnings

from views import collect_posts, client, classify_news


def fetch_and_preprocess_news():
    with client:
        client.loop.run_until_complete(collect_posts())


if __name__ == '__main__':
    fetch_and_preprocess_news()
    classify_news()
