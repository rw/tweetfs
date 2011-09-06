# pack a file or directory into a dict
from bitstring import BitArray
import bson
from os.path import exists, split
import os

def fatal_if_nexists(name, kind):
    '''Fail if a file does not exist.'''
    if not exists(name):
       raise RuntimeError('FATAL: %s "%s" does not exist' % (kind, name))

def serialize(x):
    s = bson.dumps(x)
    print 'serialized payload for twitter: %s bytes -> %s bytes' % (len(x), len(s))
    if not type(s) is str:
        raise ArgumentError('FATAL: bad string "%s"' % s)
    return s

def read_file(name):
    fatal_if_nexists(name, 'file')
    print ('reading file "%s"...' % name),
    raw = open(name, 'rb').read()
    print 'ok'
    return raw

def dirs(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def files(dir):
    return [name for name in os.listdir(dir)
            if os.path.isfile(os.path.join(dir, name))]

def pack(node, uploader, concealer):
    if os.path.isfile(node):
        serialized_payload = BitArray(bytes=serialize({'type': 'file',
                                                       'name': node,
                                                       'data': read_file(node)}))
        hidden_payload = concealer.conceal(serialized_payload)
        external_id = uploader(hidden_payload)
        print 'packed "%s" and uploaded as tweet_id %s' % (node, external_id)
        return external_id
    else:
        os.chdir(node)
        external_ids = []
        for child in os.listdir('.'):
            external_ids.append(pack(child, uploader, concealer))
        os.chdir('..')
        serialized_payload = BitArray(bytes=serialize({'type': 'dir',
                                                       'name': node,
                                                       'ids': external_ids}))
        hidden_payload = concealer.conceal(serialized_payload)
        external_id = uploader(hidden_payload)
        print 'packed "%s" and uploaded as tweet_id %s' % (node, external_id)
        return external_id
