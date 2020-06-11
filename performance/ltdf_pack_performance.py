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

PACK_KEY_FILE = "ltdf_pack_key_{}.p".format(MAX_BIT_LEN)
PACK_CT_FILE = "ltdf_pack_ct_{}.p".format(MAX_BIT_LEN)

setup = "from lossy_tdf import LTDFCodec, IndexKey, TrapdoorKey, LTDFMatrix"
statement = "a = LTDFCodec.deserialize('{}')".format(KEY_FILE)
time = timeit.timeit(statement, setup, number=10)
print("unpack LTDFCodec: {} s".format(time))

setup = "from lossy_tdf import LTDFCipherText"
statement = "a = LTDFCipherText.deserialize('{}')".format(CT_FILE)
time = timeit.timeit(statement, setup, number=100)
print("unpack LTDFCipherText: {} s".format(time))

setup = "from lossy_tdf import LTDFCodec, IndexKey, TrapdoorKey, LTDFMatrix; a = LTDFCodec.deserialize('{}')".format(KEY_FILE)
statement = "a.serialize('{}')".format(PACK_KEY_FILE)
time = timeit.timeit(statement, setup, number=10)
print("pack LTDFCodec: {} s".format(time))

setup = "from lossy_tdf import LTDFCipherText; a = LTDFCipherText.deserialize('{}')".format(CT_FILE)
statement = "a.serialize('{}')".format(PACK_CT_FILE)
time = timeit.timeit(statement, setup, number=100)
print("pack LTDFCipherText: {} s".format(time))

"""
unpack LTDFCodec: 14.749693202786148 s
unpack LTDFCipherText: 0.005489026196300983 s
pack LTDFCodec: 17.534164390526712 s
pack LTDFCipherText: 0.052633848041296005 s
"""
