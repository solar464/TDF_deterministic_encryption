import sys
sys.path.append("..")
sys.path.append("../..")
from lossy_tdf import LTDFCodec
from BEC import BECCodec
import pickle

"""
Use to generate fresh LTDFCodec and LTDFCipherText for testing.
"""

if __name__ == "__main__":
    bec = BECCodec(c=3,nsym=3,t=10)
    x = [0,1,2]
    ltdf = LTDFCodec(max_len = len(bec.encode(x)))

    u = ltdf.encode(x, bec)
    result = ltdf.decode(u)
    
    with open("ltdf_test_ct.p", "wb") as f:
        pickle.dump(u, f)
    with open("ltdf_test_keys.p", "wb") as f:
        pickle.dump(ltdf, f)
