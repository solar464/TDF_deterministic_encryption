import unittest
import pickle
from bitarray import bitarray

from floodberry.floodberry_ed25519 import GE25519 as GE
from ddh_tdf import TDFVector, TDFError
from utils import serialize, deserialize

VECTOR_TEST_SERIALIZE_FILE = "tests/tdf_test_vector.p"
ONE = [1, 0, 0, 0, 0]

VECTOR_SIZE = 3
VECTOR = TDFVector(VECTOR_SIZE)
#[ 1, 3, 5, ...]
for i in range(VECTOR_SIZE):
    VECTOR.set(i, GE(2*i + 1))

#[ 0, 1, 0, 1 ...]
DOT_TEST = [0, 1] * (VECTOR_SIZE // 2) + [0] * (VECTOR_SIZE % 2)
DOT_TEST_R = sum([i for i in range(3, 2 * VECTOR_SIZE, 4)])

class TestTDFVector(unittest.TestCase):
    def test_copy(self):
        n_vector = VECTOR.copy()
        self.assertEqual(n_vector, VECTOR)

        n_vector.scale(2)
        self.assertNotEqual(n_vector, VECTOR)

    def test_all_to_affine(self):
        VECTOR.all_to_affine()
        
        self.assertTrue(all([g.z == ONE for g in VECTOR.M]))
        self.assertTrue(VECTOR.all_validate())

    def test_serialization(self):
        serialize(VECTOR, VECTOR_TEST_SERIALIZE_FILE)
        n_vector = deserialize(VECTOR_TEST_SERIALIZE_FILE)
        
        VECTOR.all_to_affine()
        
        self.assertEqual(n_vector, VECTOR)
        self.assertTrue(VECTOR.all_validate())
        self.assertTrue(n_vector.all_validate())

    def test_dot(self):
        self.assertRaises(TDFError, VECTOR.dot, bitarray(1) * (VECTOR_SIZE + 1))
        
        hashed = VECTOR.dot(DOT_TEST).to_affine()
        self.assertEqual(hashed, GE(DOT_TEST_R).to_affine())

        short_dot = VECTOR.dot([0]).to_affine()
        self.assertEqual(short_dot, GE(0).to_affine())
    
    def test_scale(self):
        n_vector = VECTOR.copy()
        n_vector.scale(42)
        scaled_hash = n_vector.dot(DOT_TEST).to_affine()
        self.assertEqual(scaled_hash, GE(DOT_TEST_R * 42).to_affine())
        self.assertTrue(VECTOR.all_validate())
        self.assertTrue(n_vector.all_validate())

