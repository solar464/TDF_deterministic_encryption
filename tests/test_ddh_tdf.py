import unittest
import pickle
from array import array

from floodberry.floodberry_ed25519 import GE25519
from ddh_tdf import TDFError, TDFVector, KG, DDH_TDF_IndexKey, DDH_TDF_TrapdoorKey, DDH_TDF_CipherText as CipherText
from utils import deserialize, serialize

TEST_DIR = "tests/"

PACK_TEST_IK_FILE = TEST_DIR + "tdf_pack_test_ik.p"
PACK_TEST_TK_FILE = TEST_DIR + "tdf_pack_test_tk.p"
PACK_TEST_CT_FILE = TEST_DIR + "tdf_pack_test_ct.p"
TDF_MSG_FILE = TEST_DIR + "tdf_test_msg.p"
TDF_IK_FILE = TEST_DIR + "tdf_test_ik.p"
TDF_TK_FILE = TEST_DIR + "tdf_test_tk.p"
TDF_CT_FILE = TEST_DIR + "tdf_test_ct.p"
"""
x = b'\x00\x01\x02'
ik, tk = KG(len(x) * 8)

u = ik.encode(x)
result = tk.decode(u)
"""
IK = deserialize(TDF_IK_FILE)
TK = deserialize(TDF_TK_FILE)
CT = deserialize(TDF_CT_FILE)
X  = deserialize(TDF_MSG_FILE)

class TestDDHTDF(unittest.TestCase):
    def test_packing(self):
        ik, tk = KG(length=8)
        u = ik.encode(b'\x0f')

        serialize(ik, PACK_TEST_IK_FILE)
        serialize(tk, PACK_TEST_TK_FILE)
        serialize(u, PACK_TEST_CT_FILE)

        ik1 = deserialize(PACK_TEST_IK_FILE)
        tk1 = deserialize(PACK_TEST_TK_FILE)
        u1  = deserialize(PACK_TEST_CT_FILE)
        
        #call to_affine on all GE objects in codec
        self.assertEqual(u.all_to_affine(), u1)
        self.assertEqual(ik.all_to_affine(), ik1)
        self.assertEqual(tk.all_to_affine(), tk1)
    
    def test_encode(self):
        ct = IK.encode(X)
        self.assertEqual(ct.all_to_affine(), CT.all_to_affine())
    
    def test_decode(self):
        result = TK.decode(CT)
        self.assertEqual(X, result)

    def test_different_length_encode_decode(self):
        ct_short = IK.encode(b'\x0f')
        self.assertEqual(TK.decode(ct_short), b'\x0f')

        self.assertRaises(TDFError, IK.encode, b'\x0f' * 100)
