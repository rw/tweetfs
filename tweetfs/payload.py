from bitstring import ConstBitArray
import bson, os

import fs

def write_payload(payload):
    x = payload
    print x
    for k in ['type', 'name']:
        if k not in x:
            raise RuntimeError('FATAL: bad BSON block: %s not in %s' %
                               (k, x.keys()))
    if x['type'] == 'file':
        fs.write_file(x['name'], x['data']) # raw bytes
    elif x['type'] == 'dir':
        fs.create_dir(x['name'])
        os.chdir(x['name'])
        for child in x.get('children', []):
            payload = fetch_payload(child) # twitter id
            write_payload(bson.loads(payload))
        os.chdir('..')

if __name__ == '__main__':
    f0 = bson.dumps({'type': 'file',
                     'name': 'foo',
                     'data': ConstBitArray('0xabcdef').tobytes()})
    f1 = bson.dumps({'type': 'file',
                     'name': 'qu ux',
                     'data': ConstBitArray('0x012345678').tobytes()})
    d0 = bson.dumps({'type': 'dir',
                     'name': 'baz',
                     'children': ['abc', 'xyz']})
    def fetch_payload(tweet_id): # dummy, for testing. hooray dynamic scope
        if tweet_id == 'abc':
            return f0
        elif tweet_id == 'xyz':
            return f1

    write_payload(bson.loads(d0))

    print 'contents of directory baz/:'
    os.system('ls -l baz | sed 1d')
