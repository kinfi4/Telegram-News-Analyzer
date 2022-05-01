from views import collect_posts, client


with client:
    client.loop.run_until_complete(collect_posts())
