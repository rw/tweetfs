# unpack a dict into a dir or file
import bson
from os.path import exists
from os import chdir, mkdir, tmpfile

from bitstring import ConstBitArray
from util import is_file, is_dir, assert_type


def fatal_if_exists(name, kind):
    '''Fail if a file exists.'''
    if exists(name):
       raise RuntimeError('FATAL: %s "%s" already exists' % (kind, name))

def deserialize(s):
    x = bson.loads(s)
    if not is_file(x) and not is_dir(x):
        raise ArgumentError('FATAL: bad type "%s"' % x['type'])
    return x

def unpack(payload, downloader, concealer, name_override=None, recur=False):
    print str(payload)
    assert_type(payload, dict, 'unpack')

    if is_file(payload):
        data, name = payload['data'], payload['name']
        if name_override:
            name = name_override
        fatal_if_exists(name, 'file')
        print 'writing "%s"' % name
        write_file(name, data)
    elif is_dir(payload):
        ids, name = payload['ids'], payload['name']
        if name_override:
            name = name_override
        fatal_if_exists(name, 'directory')
        print 'name: %s, tweet_ids: %s' % (name, ids)
        write_dir(name)
        if recur:
            chdir(name)
            for id in ids:
                unpack(concealer.reveal(deserialize(downloader(id)),
                                                    downloader,
                                                    name_override=None,
                                                    recur=recur))
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
