import sys
sys.path.append("..")
from ddh_tdf import KG
import pickle

"""
Use to generate fresh TDFCodec and TDFCipherText for testing.
"""

if __name__ == "__main__":
    x = b'\x00\x01\x02'
    ik, tk = KG(length = len(x) * 8)

    u = ik.encode(x)
    result = tk.decode(u)
    
    with open("tdf_test_msg.p", "wb") as f:
        pickle.dump(x, f)
    with open("tdf_test_ct.p", "wb") as f:
        pickle.dump(u, f)
    with open("tdf_test_ik.p", "wb") as f:
        pickle.dump(ik, f)
    with open("tdf_test_tk.p", "wb") as f:
        pickle.dump(tk, f)
