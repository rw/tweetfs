# pack a file or directory into a dict
import bson
from os.path import exists, split
import os

def fatal_if_nexists(name, kind):
    '''Fail if a file does not exist.'''
    if not exists(name):
       raise RuntimeError('FATAL: %s "%s" does not exist' % (kind, name))

def serialize(x):
    s = bson.dumps(x)
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

def pack(node, uploader):
    if os.path.isfile(node):
        print 'file: %s' % node
        payload = serialize({'type': 'file',
                             'name': node,
                             'data': read_file(node)})
        external_id = uploader(payload)
        return external_id
    else:
        print 'dir: %s: %s' % (node, os.listdir(node))
        os.chdir(node)
        external_ids = []
        for child in os.listdir('.'):
            external_ids.append(pack(child, uploader))
        os.chdir('..')
        payload = serialize({'type': 'dir',
                             'name': node,
                             'ids': external_ids})
        external_id = uploader(payload)
        return external_id
