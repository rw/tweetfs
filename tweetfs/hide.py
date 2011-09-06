import plainsight as PS
from bitstring import BitArray
import os, sys
from glob import glob
import marshal as pickle

from util import assert_type

class Concealer(object):
    def __init__(self):
        self.context = 2
        self.model = self.create_model()

#       TODO: caching
#       self.model_filename = os.path.expanduser('~/.tweetfs/lang-model.pickle')
#       if not os.path.exists(self.model_filename):
#           self.create_model()
#       self.load_cached_model()

    def load_cached_model(self):
        print 'loading cached language model from %s...' % self.model_filename,
        self.model = pickle.load(open(self.model_filename, 'rb'))
        print 'done'

    def create_model(self):
        print 'creating language model: ',
        sys.stdout.flush()
        model = PS.model.Model(self.context, progress=False)
        filenames = glob(os.path.expanduser('~/.tweetfs/texts/*.txt'))
        text = ' '.join(map(lambda fn: open(fn, 'r').read(), filenames))
        print 'input is %s bytes, loading into model... ' % len(text),
        sys.stdout.flush()

        model.add_text(text, self.context)
        print 'done'
        return model

    def conceal(self, cleartext, do_test=True):
        assert_type(cleartext, BitArray, 'conceal input')
        ciphertext = PS.model.cipher(self.model,
                                     self.context,
                                     cleartext,
                                     'encipher')
        assert_type(ciphertext, str, 'conceal output')
        if do_test:
            sink = open('/dev/null', 'w')
            out, err  = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = sink, sink
            test = self.reveal(ciphertext, do_test=False)
            sys.stdout, sys.stderr = out, err
            sink.close()
            if test != cleartext:
                raise RuntimeError('conceal+reveal did not produce expected output')
        print 'concealed cleartext, output is %s bytes' % len(ciphertext)
        return ciphertext

    def reveal(self, ciphertext, do_test=True):
        assert_type(ciphertext, str, 'reveal input')
        cleartext = PS.model.cipher(self.model,
                                    self.context,
                                    ciphertext.split(),
                                    'decipher')
        assert_type(cleartext, BitArray, 'reveal output')
        if do_test:
            sink = open('/dev/null', 'w')
            out, err  = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = sink, sink
            test = self.conceal(cleartext, do_test=False)
            sys.stdout, sys.stderr = out, err
            sink.close()
            if test != ciphertext:
                raise RuntimeError('reveal+conceal did not produce expected output')
        print 'revealed ciphertext, output is %s bytes' % len(cleartext)
        return cleartext
