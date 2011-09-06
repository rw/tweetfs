# unpack a dict into a dir or file
from bitstring import BitArray
import bson
from os.path import exists
from os import chdir, chmod, mkdir, tmpfile

from util import is_file, is_dir, assert_type


def fatal_if_exists(name, kind):
    '''Fail if a file exists.'''
    if exists(name):
       raise RuntimeError('FATAL: %s "%s" already exists' % (kind, name))

def deserialize(bits):
    assert_type(bits, BitArray, 'deserialize')
    s = bits.tobytes()
    assert_type(s, str, 'deserialize')
#   print 'serialized payload from twitter: %s bytes -> %s bytes' % \
#          (len(bits) / 8.0, len(s))
    print 'serialized payload from twitter: %s bytes' % len(s)
    x = bson.loads(s)
    if not is_file(x) and not is_dir(x):
        raise ArgumentError('FATAL: bad type "%s"' % x['type'])
    return x

def unpack(payload, tweet_id, downloader, concealer, name_override=None, recur=False):
    assert_type(payload, dict, 'unpack')

    if is_file(payload):
        data, name, perms = payload['data'], payload['name'], int(payload['perms'])
        if name_override:
            name = name_override
        fatal_if_exists(name, 'file')
        print 'unpacked "%s" from tweet_id %s' % (name, tweet_id)
        write_file(name, data)
        print 'permissions: %s' % perms
        chmod(name, perms)
        print ''
    elif is_dir(payload):
        ids, name, perms = payload['ids'], payload['name'], int(payload['perms'])
        if name_override:
            name = name_override
        fatal_if_exists(name, 'directory')
        print 'unpacked "%s" with child tweet_ids %s' % (name, ids)
        write_dir(name)
        print 'permissions: %s' % perms
        chmod(name, perms)
        print ''
        if recur:
            chdir(name)
            for tweet_id in ids:
                payload = downloader(tweet_id)
                payload = concealer.reveal(payload)
                payload = deserialize(payload)
                unpack(payload,
                       tweet_id,
                       downloader,
                       concealer,
                       name_override=None,
                       recur=recur)
            chdir('..')

def write_file(name, data):
    '''create file on filesystem
       name + bits -> fd'''
    fatal_if_exists(name, 'file')
    print 'creating "%s" (%s bytes)...' % (name, len(data)),
    f = open(name, 'wb') # simple. TODO: metadata support
    f.write(data)
    f.close()
    print 'ok'

def write_dir(name):
    '''create dir on filesystem'''
    fatal_if_exists(name, 'directory')
    print ('creating directory "%s"...' % name),
    mkdir(name) # uses umask and current working dir
    print 'ok'
