import os
import bson
import shutil
import subprocess
from pack import pack
from unpack import unpack

def are_identical_dirs(d0, d1):
    retcode = subprocess(["diff", d0, d1])
    if retcode == 0:
        return True
    else:
        return False

def fixture():
    os.mkdir('unit-test-src/')
    os.mkdir('unit-test-src/bar/')
    os.mkdir('unit-test-src/bar/quux')
    os.chdir('unit-test-src')
    foo = ConstBitArray(hex='0x031337').tobytes()
    baz = ConstBitArray(hex='0x01234567').tobytes()
    waldo = ConstBitArray(hex='').tobytes()
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
    encoded = pack(TEST_SRC)
    unpack(encoded, TEST_DEST1)
    if not are_identical_dirs(TEST_SRC, TEST_DEST1):
        raise RuntimeError('%s is diff than %s, packing test failed' % \
                (TEST_SRC, TEST_DEST1))
    else:
        print 'TEST 1: PASSED'

    # test2: transitivity is fun
    encoded2 = pack(TEST_DEST1)
    unpack(encoded2, TEST_DEST2)
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

fixture()
verify()
