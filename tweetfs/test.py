import os
import bson
import shutil
import subprocess
from bitstring import ConstBitArray
from comm import *
from pack import pack, serialize
from unpack import unpack

TEST_SRC = 'unit-test-src'
TEST_DEST1 = 'unit-test-dest1'
TEST_DEST2 = 'unit-test-dest2'

def are_identical_dirs(d0, d1):
    retcode = subprocess(["diff -r", d0, d1])
    if retcode == 0:
        return True
    else:
        return False

def verify_comms(uploader, downloader):
    waldo = ConstBitArray(hex='0x0001').tobytes()
    x = serialize({'type': 'file',
                   'name': 'waldo',
                   'data': waldo})
    i = uploader(x)
    out = downloader(i)
    assert(out == x)

def fixture():
    os.mkdir(TEST_SRC)
    os.mkdir(TEST_SRC + '/bar')
    os.mkdir(TEST_SRC + '/bar/quux')
    os.chdir(TEST_SRC)
    foo = ConstBitArray(hex='0x031337').tobytes()
    baz = ConstBitArray(hex='0x01234567').tobytes()
    waldo = ConstBitArray(hex='0x0001').tobytes()
    f = open('foo', 'wb'); f.write(foo); f.close()
    os.chdir('bar')
    f = open('baz', 'wb'); f.write(baz); f.close()
    os.chdir('quux')
    f = open('waldo', 'wb'); f.write(waldo); f.close()
    os.chdir('../../..')

def file_equals(filename, bytestr):
    return open(filename, 'rb').read() == bytestr

def verify():
    # test1: test that a packed dir gets unpacked correctly
    tweet_id = pack(TEST_SRC, memory_uploader)
    return
    unpack(tweet_id, TEST_DEST1, downloader=memory_downloader)
    if not are_identical_dirs(TEST_SRC, TEST_DEST1):
        raise RuntimeError('%s is diff than %s, packing test failed' % \
                (TEST_SRC, TEST_DEST1))
    else:
        print 'TEST 1: PASSED'

    return
    # test2: transitivity is fun
    encoded2 = pack(TEST_DEST1)
    unpack(encoded2, TEST_DEST2, downloader=memory_downloader)
    if not are_identical_dirs(TEST_SRC, TEST_DEST2):
        raise RuntimeError('%s is diff than %s, packing test failed' % \
                (TEST_SRC, TEST_DEST2))
    else:
        print 'TEST 2: PASSED'

    # cleanup
    for dname in [TEST_SRC, TEST_DEST1, TEST_DEST2]:
        print 'deleting test dir %s... ' % dname,
        shutil.mtree(dname)
        print 'ok'

verify_comms(memory_uploader, memory_downloader)
fixture()
verify()
