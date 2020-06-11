import sys
sys.path.append("..")

from lossy_tdf import LTDFCodec
from random import randint
import timeit

#key generation
setup = "from lossy_tdf import LTDFCodec;"
statement = "LTDFCodec(msg_len=3, t=10, c1=2)"
time = timeit.timeit(statement, setup, number=3)
print(time)

#encoding
setup = "from lossy_tdf import LTDFCodec; enc = LTDFCodec(msg_len=3, t=10, c1=2, lmbd=10)"
statement = "enc.encode([0,0,0])"
time = timeit.timeit(statement, setup, number=10)
print(time)

#decoding
setup = "from lossy_tdf import LTDFCodec; enc = LTDFCodec(msg_len=3, t=10, c1=2, lmbd=10); u = enc.encode([0,0,0])"
statement = "enc.decode(u)"
time = timeit.timeit(statement, setup, number=10)
print(time)


"""
191.639850074891 s
3.2787724011577666 s
0.1361908339895308 s
"""
