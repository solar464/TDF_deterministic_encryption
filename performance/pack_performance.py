import sys
sys.path.append("..")
import timeit

from benchmark_constants import IK_FILE, TK_FILE, CT_FILE, PACK_UNPACK_REPEAT as REPEAT_NUM

"""
Benchmarks serialization of ddh tdf keys and ciphertext.
"""
for f in [IK_FILE, TK_FILE, CT_FILE]:
    setup = "from utils import serialize, deserialize"
    statement = "a = deserialize('{}')".format(f)
    time = timeit.timeit(statement, setup, number=REPEAT_NUM)
    print("{} unpack {} times: {} s".format(f, REPEAT_NUM, time))

    setup = "from utils import serialize, deserialize; a = deserialize('{}')".format(f)
    statement = "serialize(a, 'tmp.p')".format(f)
    time = timeit.timeit(statement, setup, number=REPEAT_NUM)
    print("{} pack   {} times: {} s".format(f, REPEAT_NUM, time))

"""
32 BYTE MSG

ddh_tdf_ik.p unpack 10 times: 5.349741816520691 s
ddh_tdf_ik.p pack   10 times: 6.298587778583169 s
ddh_tdf_tk.p unpack 10 times: 0.0009995289146900177 s
ddh_tdf_tk.p pack   10 times: 0.014318365603685379 s
ddh_tdf_ct.p unpack 10 times: 0.0007096044719219208 s
ddh_tdf_ct.p pack   10 times: 0.002279512584209442 s
"""
