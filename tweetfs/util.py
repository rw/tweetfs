def is_file(x):
    return x['type'] == 'file'

def is_dir(x):
    return x['type'] == 'dir'

def assert_type(x, expected_type, prefix='generic error'):
    if type(x) != expected_type:
        raise RuntimeError('%s: expected %s, got %s' % \
                           (prefix, expected_type, type(x)))
