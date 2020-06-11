import sys, os
sys.path.append('..')
import timeit

from benchmark_constants import MSG_FILE, IK_FILE, TK_FILE, CT_FILE, ENCODE_DECODE_REPEAT as REPEAT_NUM

"""
Benchmarks serialization of lossy tdf key and ciphertext.
"""
setup="from utils import deserialize; "
setup += "ik = deserialize('{}'); \
          msg = deserialize('{}');".format(IK_FILE, MSG_FILE)

statement = "ik.encode(msg)"
time = timeit.timeit(statement, setup, number=REPEAT_NUM)
print("encode {} times: {} s".format(REPEAT_NUM, time))

setup="from utils import deserialize;"
setup += "a = deserialize('{}'); \
          u = deserialize('{}');".format(TK_FILE, CT_FILE)

statement = "a.decode(u)"
time = timeit.timeit(statement, setup, number=100)
print("decode {} times: {} s".format(REPEAT_NUM, time))

"""
encode 100 times: 3.072250325232744 s
decode 100 times: 1.7979607712477446 s
"""
