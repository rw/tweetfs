from bitstring import ConstBitArray
import bson, os

import pack, unpack

def write_payload(payload):
    x = payload
    for k in ['type', 'name']:
        if k not in x:
            raise RuntimeError('FATAL: bad BSON block: %s not in %s' %
                               (k, x.keys()))
    if x['type'] == 'file':
        pack.write_file(x['name'], x['data']) # raw bytes
    elif x['type'] == 'dir':
        pack.write_dir(x['name'])
        os.chdir(x['name'])
        for child in x.get('children', []):
            payload = fetch_payload(child) # twitter id
            write_payload(bson.loads(payload))
        os.chdir('..')

def file_payload(name):
    # files only this version
    raw = pack.read_file(name)
    d = bson.dumps({'type': 'file',
                    'name': name,
                    'data': raw})
    return d

def dir_payload(name, tweet_ids):
    d = bson.dumps({'type': 'dir',
                    'name': name,
                    'ids': tweet_ids})
    return d


def dir_to_payloads(name):
    for basedir, dirs_unused, files in os.walk(name, topdown=False):
        print 'entering: %s' % basedir
        tweet_ids = []
        for i, f in enumerate(files):
            print 'uploading file named: "%s" ...' % f,
            file_payload(os.path.join(basedir, f))
            tweet_ids.append(i)
        print ('uploading dir listing: "%s" ...' % basedir),
        dir_payload(basedir, tweet_ids)
#       print 'ok'

if __name__ == '__main__':
    dir_to_payloads('.')
#   
#   f0 = bson.dumps({'type': 'file',
#                    'name': 'foo',
#                    'data': ConstBitArray('0xabcdef').tobytes()})
#   f1 = bson.dumps({'type': 'file',
#                    'name': 'qu ux',
#                    'data': ConstBitArray('0x012345678').tobytes()})
#   d0 = bson.dumps({'type': 'dir',
#                    'name': 'baz',
#                    'children': ['abc', 'xyz']})
#   def fetch_payload(tweet_id): # dummy, for testing. hooray dynamic scope
#       if tweet_id == 'abc':
#           return f0
#       elif tweet_id == 'xyz':
#           return f1

#   write_payload(bson.loads(d0))

#   print 'contents of directory baz/:'
#   os.system('ls -l baz | sed 1d')
