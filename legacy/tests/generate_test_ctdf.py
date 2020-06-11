import sys
sys.path.append("..")
sys.path.append("../..")
from complete_tdf import CTDFCodec
import pickle

"""
Use to generate fresh LTDFCodec and LTDFCipherText for testing.
"""

if __name__ == "__main__":
    x = [0,1,2]
    ctdf = CTDFCodec(max_len = len(x) * 3)

    u = ctdf.encode(x, c=3)
    result = ctdf.decode(u)
    
    with open("ctdf_test_ct.p", "wb") as f:
        pickle.dump(u, f)
    with open("ctdf_test_keys.p", "wb") as f:
        pickle.dump(ctdf, f)
