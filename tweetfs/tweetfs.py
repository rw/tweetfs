import sys
from bitstring import BitArray
from pack import pack, serialize
from unpack import unpack, deserialize
from hide import Concealer
from twitter import make_client, make_downloader, make_uploader

def upload(fn, uploader, concealer):
    ''' fn: a filename or dirnname '''
    print 'uploading'
    tweet_id = pack(fn, uploader, concealer)
    print tweet_id

def download(tweet_id, downloader, concealer, name_override=False):
    print 'downloading'
    root = deserialize(concealer.reveal(downloader(tweet_id)).tobytes())
    unpack(root, downloader, concealer, name_override, True)
    print 'done'

mode = sys.argv[1]
concealer = Concealer()
concealer.model_load()
client = make_client()
if mode == 'upload':
    fn = sys.argv[2]
    upload(fn, make_uploader(client), concealer)
elif mode == 'download':
    tweet_id = sys.argv[2]
    target_fn = sys.argv[3]
    download(tweet_id, make_downloader(client),
             concealer, name_override=target_fn)
