# unpack a dict into a dir or file
import bson
from os.path import exists
from os import chdir, mkdir, tmpfile

from bitstring import ConstBitArray

from util import is_file, is_dir


def fatal_if_exists(name, kind):
    '''Fail if a file exists.'''
    if exists(name):
       raise RuntimeError('FATAL: %s "%s" already exists' % (kind, name))

def deserialize(s):
    x = bson.loads(s)
    if not is_file(x) and not is_dir(x):
        raise ArgumentError('FATAL: bad type "%s"' % x['type'])
    return x

def unpack(x, retrieve, recur=False):
    '''Option: recur=True will unpack all data.'''
    if is_file(x):
        data, name = x['data'], x['name']
        write_file(name, data)
    elif is_dir(x):
        name, tweet_ids = x['name'], x['ids']
        write_dir(name)
        if recur:
            chdir(name)
            for tweet_id in tweet_ids:
                unpack(deserialize(retrieve(tweet_id)),
                       retrieve,
                       recur=recur)
            chdir('..')

def write_file(name, data):
    '''create file on filesystem
       name + bits -> fd'''
    fatal_if_exists(name, 'file')
    print 'creating "%s" (%s bytes)...' % (name, len(data)),
    f = open(name, 'w') # simple. TODO: metadata support
    f.write(data)
    f.close()
    print 'ok'

def write_dir(name):
    '''create dir on filesystem'''
    fatal_if_exists(name, 'directory')
    print ('creating directory "%s"...' % name),
    mkdir(name) # uses umask and current working dir
    print 'ok'
