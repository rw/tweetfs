import os
import bson
import shutil
import subprocess
from bitstring import ConstBitArray
from comm import *
from pack import pack, serialize
from unpack import unpack, deserialize
from hide import Concealer

TEST_SRC = 'unit-test-src'
TEST_DIR_DEST = 'unit-test-dest1'
TEST_FILE_DEST = 'unit-test-dest2'

def are_identical_dirs(d0, d1):
    return subprocess.call(['diff', '-r', d0, d1]) == 0

def verify_comms(uploader, downloader, concealer):
    waldo = ConstBitArray(hex='0x0001').tobytes()
    payload = serialize({'type': 'file',
                         'name': 'waldo',
                         'data': waldo})
    payload = concealer.conceal(payload)
    upload_id = uploader(payload)
    downloaded = downloader(upload_id)
    downloaded = concealer.reveal(downloaded)
    assert(payload == downloaded)

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

def verify_file():
    # test1: test that a packed file gets unpacked correctly
    fn = TEST_SRC + '/foo'
    tweet_id = pack(fn, memory_uploader)
    payload = deserialize(memory_downloader(tweet_id))
    unpack(payload, memory_downloader, name_override=TEST_FILE_DEST , recur=True)
    if not are_identical_dirs(fn, TEST_FILE_DEST):
        raise RuntimeError('%s is diff than %s, packing test failed' % \
                (fn, TEST_FILE_DEST))
    else:
        print 'TEST 1: PASSED'

def verify_dir():
    # test2: test that a packed dir gets unpacked correctly
    tweet_id = pack(TEST_SRC, memory_uploader)
    root_payload = deserialize(memory_downloader(tweet_id))
    unpack(root_payload, memory_downloader, name_override=TEST_DIR_DEST, recur=True)
    if not are_identical_dirs(TEST_SRC, TEST_DIR_DEST):
        raise RuntimeError('%s is diff than %s, packing test failed' % \
                (TEST_SRC, TEST_DIR_DEST))
    else:
        print 'TEST 2: PASSED'

def cleanup():
    # cleanup fixtures
    for dname in [TEST_SRC, TEST_DIR_DEST]:
        print 'deleting test dir %s... ' % dname,
        shutil.rmtree(dname)
        print 'ok'
    for fname in [TEST_FILE_DEST]:
        print 'deleting test file %s... ' % fname,
        os.remove(fname)
        print 'ok'


c = Concealer()
c.model_load()
verify_comms(memory_uploader, memory_downloader, c)
fixture()
verify_file()
verify_dir()
cleanup()
