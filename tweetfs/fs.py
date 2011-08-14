from bitstring import ConstBitArray
from os import mkdir, tmpfile
from os.path import exists

def fatal_if_exists(name, kind):
    if exists(name):
       raise RuntimeError('FATAL: %s "%s" already exists!' % (kind, name))

def fatal_if_nexists(name, kind):
    if not exists(name):
       raise RuntimeError('FATAL: %s "%s" does not exist!' % (kind, name))

def read_file(name):
    fatal_if_nexists(name, 'file')
    print ('reading file "%s"...' % name),
    raw = open(name, 'rb').read()
    print 'ok'
    return raw

#def read_dir(name):
#    fatal_if_nexists(name, 'directory')
#    print ('reading directory "%s"...' % name),
#    raw = open(name, 'rb').read()
#    print 'ok'
#    return raw

# create dir on filesystem
def write_dir(name):
    fatal_if_exists(name, 'directory')
    print ('creating directory "%s"...' % name),
    mkdir(name) # uses umask and current working dir
    print 'ok'

# create file on filesystem
def write_file(name, data):
    """name + bits -> fd"""
    fatal_if_exists(name, 'file')
    print 'creating "%s" (%s bytes)...' % (name, len(data)),
    f = open(name, 'w') # simple. TODO: metadata support
    f.write(data)
    f.close()
    print 'ok'

if __name__ == '__main__':
    data = open('fs.py').read()
    bits = ConstBitArray(bytes=data)
    write_file('hey', bits.tobytes())
