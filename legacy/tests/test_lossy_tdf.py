import unittest
import pickle
from array import array
import lossy_tdf

import floodberry
from floodberry.floodberry_ed25519 import GE25519
from BEC import BECCodec, BECError
from tdf_strucs import TDFMatrix, TDFError
from lossy_tdf import LTDFCodec as Codec, LTDFCipherText as CipherText

TEST_DIR = "legacy/tests/"

PACK_TEST_KEY_FILE = TEST_DIR + "ltdf_pack_test_keys.p"
PACK_TEST_CT_FILE = TEST_DIR + "ltdf_pack_test_ct.p"
TDF_KEY_FILE = TEST_DIR + "ltdf_test_keys.p"
TDF_CT_FILE = TEST_DIR + "ltdf_test_ct.p"
"""
bec = BECCodec(c=3, nsym=3, t=10)
x = [0,1,2]
ltdf = LTDFCodec(len(bec.encode(x)))
 
u = ltdf.encode(x)
result = ltdf.decode(u)
"""
TDF = Codec.deserialize(TDF_KEY_FILE)
CT = CipherText.deserialize(TDF_CT_FILE)
X = array('i', [0,1,2])
BEC = CT.get_BECCodec()

class TestLTDF(unittest.TestCase):
    def test_packing(self):
        bec = BECCodec(c = 4, nsym = 1, t=2)
        tdf = Codec(16)
        u = tdf.encode(array('i',[1]), bec)

        tdf.serialize(PACK_TEST_KEY_FILE)
        u.serialize(PACK_TEST_CT_FILE)

        tdf1 = Codec.deserialize(PACK_TEST_KEY_FILE)
        u1 = CipherText.deserialize(PACK_TEST_CT_FILE)
        
        #call to_affine on all GE objects in codec
        self.assertEqual(u.all_to_affine(), u1)
        self.assertEqual(tdf.all_to_affine(), tdf1)
    
    def test_encode(self):
        ct = TDF.encode(X, BEC)
        self.assertEqual(ct.all_to_affine(), CT.all_to_affine())
    
    def test_decode(self):
        result = TDF.decode(CT)
        self.assertEqual(X, result)

    def test_different_length_encode_decode(self):
        ct_short = TDF.encode([2], BEC)
        self.assertEqual(TDF.decode(ct_short), array('i', [2]))

        self.assertRaises(TDFError, TDF.encode, [3] * 100, BEC)
