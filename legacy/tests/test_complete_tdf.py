import unittest
import pickle
from array import array
import complete_tdf

from floodberry.floodberry_ed25519 import GE25519
from tdf_strucs import TDFMatrix, TDFError
from complete_tdf import CTDFCodec as Codec, CTDFCipherText as CipherText
from utils import int_lst_to_bitarr

TEST_DIR = "legacy/tests/"

PACK_TEST_KEY_FILE = TEST_DIR + "ctdf_pack_test_keys.p"
PACK_TEST_CT_FILE = TEST_DIR + "ctdf_pack_test_ct.p"
TDF_KEY_FILE = TEST_DIR + "ctdf_test_keys.p"
TDF_CT_FILE = TEST_DIR + "ctdf_test_ct.p"
"""
x = [0,1,2]
ctdf = CTDFCodec(len(x)*8)
 
u = ctdf.encode(x)
result = ctdf.decode(u)
"""
TDF = Codec.deserialize(TDF_KEY_FILE)
CT = CipherText.deserialize(TDF_CT_FILE)
X = int_lst_to_bitarr([0,1,2], 3)

class TestCTDF(unittest.TestCase):
    def test_packing(self):
        tdf = Codec(16)
        u = tdf.encode(array('i',[1, 2]))

        tdf.serialize(PACK_TEST_KEY_FILE)
        u.serialize(PACK_TEST_CT_FILE)

        tdf1 = Codec.deserialize(PACK_TEST_KEY_FILE)
        u1 = CipherText.deserialize(PACK_TEST_CT_FILE)
        
        #call to_affine on all GE objects in codec
        self.assertEqual(u.all_to_affine(), u1)
        self.assertEqual(tdf.all_to_affine(), tdf1)
    
    def test_encode(self):
        ct = TDF.encode(X)
        self.assertEqual(ct.all_to_affine(), CT.all_to_affine())
    
    def test_decode(self):
        result = TDF.decode(CT)
        self.assertEqual(X, result)

    def test_different_length_encode_decode(self):
        ct_short = TDF.encode([2], c=3)
        self.assertEqual(TDF.decode(ct_short), int_lst_to_bitarr([2], 3))

        self.assertRaises(TDFError, TDF.encode, [3] * 100)
