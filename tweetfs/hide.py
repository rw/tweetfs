import plainsight as PS
from bitstring import BitArray

from util import assert_type

class Concealer(object):
    def __init__(self):
        self.context = 3
        self.model_input = open('data/model-text.txt', 'rb')

        self.model = PS.model.Model(self.context)
        self.model_load()

    def model_load(self):
        model_text = PS.data.take_char_input(self.model_input)
        #start = time()
        self.model.add_text(model_text, self.context)
        #sys.stderr.write('Model: %s added in %.02fs (context == %d)\n' \
        #                 % (123,#self.model_filename.name,
        #                    time() - start,
        #                    self.context))

    def conceal(self, cleartext, do_test=True):
        assert_type(cleartext, BitArray, 'conceal input')
        ciphertext = PS.model.cipher(self.model,
                                     self.context,
                                     cleartext,
                                     'encipher')
        assert_type(ciphertext, str, 'conceal output')
        if do_test:
            test = self.reveal(ciphertext, do_test=False)
            if test != cleartext:
                raise RuntimeError('conceal+reveal did not produce expected output')
        return ciphertext

    def reveal(self, ciphertext, do_test=True):
        assert_type(ciphertext, unicode, 'reveal input')
        cleartext = PS.model.cipher(self.model,
                                    self.context,
                                    ciphertext.split(),
                                    'decipher')
        assert_type(cleartext, BitArray, 'reveal output')
        if do_test:
            test = self.conceal(cleartext, do_test=False)
            if test != ciphertext:
                raise RuntimeError('reveal+conceal did not produce expected output')
        return cleartext
