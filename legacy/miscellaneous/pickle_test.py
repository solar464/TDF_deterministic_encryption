from lossy_tdf import *
from array import array
import pickle

"""
Manual testing of pickle module for serializing LTDFCodec and LTDFCipherText    classes.
Consider changing serialization format to JSON at later date.
"""

from floodberry.floodberry_ed25519 import GE25519 as GE
def serialize(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def deserialize(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

ltdf = LTDFCodec(msg_len=1,c=3,t=1,c1=2)
x = array('i',[0])
u = ltdf.encode(x)

ltdf.serialize("keys.p")
u.serialize("ct.p")

ltdf1 = LTDFCodec.deserialize("keys.p")
u1 = LTDFCipherText.deserialize("ct.p")

