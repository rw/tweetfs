import os
import ConfigParser
from seqtweet.seqtweet import SeqTweet

def read_creds():
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.tweetfs/creds.cfg')])

    return map(lambda key: config.get('Twitter', key),
               ['CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_KEY', 'ACCESS_SECRET'])

def make_client():
    client = SeqTweet(*read_creds())
    return client

def make_uploader(client):
    return lambda s: client.create(s)

def make_downloader(client):
    return lambda tweet_id: str(client.read(tweet_id))

def make_deleter(client):
    return lambda tweet_id: client.delete(tweet_id)
