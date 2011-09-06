import sys
from bitstring import BitArray
from pack import pack, serialize
from unpack import unpack, deserialize
from hide import Concealer
from twitter import make_client, make_downloader, make_uploader, make_deleter
from comm import *
from glob import glob

DRY_RUN = True

def upload(fn, uploader, concealer):
    ''' fn: a filename or dirnname '''
    print 'mode: upload'
    tweet_id = pack(fn, uploader, concealer)
    print 'done'

def download(tweet_id, downloader, concealer, name_override=False):
    print 'mode: download'
    root = deserialize(concealer.reveal(downloader(tweet_id)))#.tobytes())
    unpack(root, tweet_id, downloader, concealer, name_override=name_override, recur=True)
    print 'done'

def delete(tweet_id, deleter):
    print 'deleting tweet_id %s' % tweet_id
    print 'done: %s' % deleter(tweet_id)

if len(sys.argv) <= 2 or sys.argv[1] == 'help':
    print '''tweetfs by robert winslow
        https://github.com/rw/tweetfs

        how to use:
        tweetfs help # what you are doing now
        tweetfs [dry_run] upload <filename or dirname>
        tweetfs [dry_run] download <tweet id> [destination name]

        examples:
        echo 'hello world!' > hw && tweetfs upload hw # returns a tweet id
        tweetfs download TODO'''
    exit()

args = sys.argv[1:]
dry_run = args[0] == 'dry_run'
if dry_run:
    args = args[1:]

concealer = Concealer() # plainsight
client = make_client() # seqtweet

if dry_run:
    uploader = memory_uploader
    downloader = memory_downloader
else:
    uploader = make_uploader(client)
    downloader = make_downloader(client)

mode = args[0]
if mode == 'upload':
    fn = args[1]
    upload(fn, uploader, concealer)
elif mode == 'download':
    tweet_id = args[1]
    target_fn = args[2]
    download(tweet_id, downloader, concealer, name_override=target_fn)
#elif mode == 'build-model':
#    filenames = glob('texts/*.txt')
#    text = ' '.join(map(lambda fn: open(fn, 'r').read(), filenames))
