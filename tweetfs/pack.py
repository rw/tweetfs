# pack a file or directory into a dict
from os.path import exists

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

def pack_walk(root):
    for basedir, unused, files in os.walk(root, topdown=False):
        print 'entering: %s' % basedir
        tweet_ids = []
        for i, f in enumerate(files):
            fullpath = os.path.join(basedir, f)
            print 'yielding file named: "%s" ...' % fullpath,
            f_packed = serialize({'type': 'file',
                                  'name': f,
                                  'data': read_file(f)})
            print f
            yield f
        print ('uploading dir listing: "%s" ...' % basedir),
        d_packed = serialize({'type': 'dir',
                              'name': basedir,
                              'ids': []})

#       pack_walk(basedir)
        print 'ok'
