import sys
sys.path.append("..")
import timeit

from utils import deserialize
from benchmark_constants import MSG_FILE, KG_REPEAT as REPEAT_NUM
MAX_BYTE_LEN = len(deserialize(MSG_FILE))
"""
Benchmarks ddh tdf index and trapdoor key generation.
Number of group elements grows as N(b) = b ** 2
    where (b) is the bit length of the longest encodable ciphertext
"""

setup = "from ddh_tdf import KG"
statement = "ik, tk = KG(length = {})".format(MAX_BYTE_LEN * 8)
time = timeit.timeit(statement, setup, number=REPEAT_NUM)
print("KG for {} bits {} time/s: {} s".format(
    MAX_BYTE_LEN * 8, REPEAT_NUM, time))

"""
DDH_TDF: Generating Keys
DDH_TDF: Finished generating 256 keys
KG for 256 bits 1 time(s): 4.119450630620122 s
"""
