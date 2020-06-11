import sys
sys.path.append("..")

import timeit

from lossy_tdf import LTDFCodec

MAX_BIT_LEN = 300

KEY_FILE = "ltdf_key_{}.p".format(MAX_BIT_LEN)
CT_FILE = "ltdf_ct_{}.p".format(MAX_BIT_LEN)
"""
Generates key and ct files for use in other benchmarking files since pickle is picky about how its objects are serialized.
"""

setup = "from lossy_tdf import LTDFCodec, BECCodec"
statement = "a = LTDFCodec({});".format(MAX_BIT_LEN)
statement += "a.serialize('{}'); \
              bec = BECCodec(c=10,t=10,nsym=2); \
              a.encode([1], bec).serialize('{}')" \
              .format(KEY_FILE, CT_FILE)

time = timeit.timeit(statement, setup, number=1)
print(time)

