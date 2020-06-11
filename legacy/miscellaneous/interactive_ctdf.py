from complete_tdf import *
from bitarray import bitarray

x = [0,0,0]
ctdf = CTDFCodec(max_len=24)
u = ctdf.encode(x, 8)
r = ctdf.decode(u)
