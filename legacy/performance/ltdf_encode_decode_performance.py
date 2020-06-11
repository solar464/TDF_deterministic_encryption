import sys
sys.path.append("..")
import timeit

from lossy_tdf import LTDFCodec

MAX_BIT_LEN = 300
"""
Benchmarks serialization of lossy tdf key and ciphertext.
"""
KEY_FILE = "ltdf_key_{}.p".format(MAX_BIT_LEN)
CT_FILE = "ltdf_ct_{}.p".format(MAX_BIT_LEN)

setup="from lossy_tdf import LTDFCodec, BECCodec;"
setup += "a = LTDFCodec.deserialize('{}'); \
          x = [1]; \
          bec = BECCodec(c=10,t=10,nsym=2);".format(KEY_FILE)

statement = "a.encode(x, bec)"
time = timeit.timeit(statement, setup, number=100)
print("LTDFCodec.encode: {} s".format(time))

setup="from lossy_tdf import LTDFCodec, LTDFCipherText;"
setup += "a = LTDFCodec.deserialize('{}'); \
          u = LTDFCipherText.deserialize('{}');".format(KEY_FILE, CT_FILE)

statement = "a.decode(u)"
time = timeit.timeit(statement, setup, number=100)
print("LTDFCodec.decode: {} s".format(time))

"""
LTDFCodec.encode: 6.861012617126107 s
LTDFCodec.decode: 2.4528341880068183 s
"""
