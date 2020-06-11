import sys
sys.path.append("..")
import timeit

from lossy_tdf import LTDFCodec

MAX_BIT_LEN = 300
"""
Benchmarks lossy tdf index and trapdoor key generation.
Number of group elements grows approximately as N(b) = 2 * (b ** 2)
    where (b) is the bit length of the longest encodable ciphertext
"""

setup = "from lossy_tdf import LTDFCodec"
statement = "a = LTDFCodec({})".format(MAX_BIT_LEN)
time = timeit.timeit(statement, setup, number=1)
print(time)

"""
max bit length = 300: 10.617518580518663 s
max bit length = 1000: should be over 2 minutes
"""
