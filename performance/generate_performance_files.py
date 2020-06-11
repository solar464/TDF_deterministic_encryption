"""
Generates key and ct files for use in other benchmarking files since pickle is picky about how its objects are serialized.
"""
import sys
sys.path.append("..")

import timeit

from ddh_tdf import KG
from utils import serialize

from benchmark_constants import MSG_FILE, IK_FILE, TK_FILE, CT_FILE
max_byte_len = 32 
if len(sys.argv) > 1:
    max_byte_len = int(sys.argv[1])

msg = b'\xf0' * max_byte_len

ik, tk = KG(length = max_byte_len * 8)
u = ik.encode(msg)

serialize(msg, MSG_FILE)
serialize(ik,  IK_FILE)
serialize(tk,  TK_FILE)
serialize(u,   CT_FILE)

if tk.decode(u) != msg:
    raise ValueError("The generated ciphertext does not decode correctly.")

