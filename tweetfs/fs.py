from os import mkdir, tmpfile
from os.path import exists

def fatal_if_exists(name, kind):
    if exists(name):
       raise RuntimeError('FATAL: tried to create %s "%s", but it ' + \
                          'already exists!' % (kind, name))

def create_dir(name):
    fatal_if_exists(name, 'directory')
    print ('creating directory "%s"...' % name),
    mkdir(name) # uses umask and current working dir
    print 'ok'

def write_file(name, data):
    """name + bits -> fd"""
    fatal_if_exists(name, 'file')
    print 'creating "%s" (%s bytes)...' % (name, len(data) / 8),
    f = open(name) # simple. TODO: metadata support
    f.write(data)
    f.close()
    print 'ok'
