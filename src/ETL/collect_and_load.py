import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # we need this, in order not to print tensorflow warnings

from views import collect_posts, client


with client:
    client.loop.run_until_complete(collect_posts())
