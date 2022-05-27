import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # we need this, in order not to print tensorflow warnings

from views import fetch_and_preprocess_news, classify_news, stack_shelling_words


if __name__ == '__main__':
    print(f'PIPELINE STARTED')

    print('-' * 30)
    fetch_and_preprocess_news()

    print('-' * 30)
    classify_news()

    print('-' * 30)
    stack_shelling_words()

    print('PIPELINE ENDED')
