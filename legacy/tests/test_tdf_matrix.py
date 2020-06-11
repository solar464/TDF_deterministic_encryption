import unittest
import pickle
from bitarray import bitarray

from floodberry.floodberry_ed25519 import GE25519 as GE
from tdf_strucs import TDFMatrix, TDFError
from utils import serialize, deserialize

MATRIX_TEST_SERIALIZE_FILE = "tests/tdf_test_matrix.p"
ONE = [1, 0, 0, 0, 0]

MATRIX_SIZE = 3
MATRIX = TDFMatrix(MATRIX_SIZE)
#[ 1, 3, 5, ...]
#[ 2, 4, 6, ...]
for i in range(MATRIX_SIZE):
    MATRIX.set(i, 0, GE(2*i + 1))
    MATRIX.set(i, 1, GE(2*i + 2))

#[ 0, 1, 0, 1 ...]
DOT_TEST = [0, 1] * (MATRIX_SIZE // 2) + [0] * (MATRIX_SIZE % 2)
DOT_TEST_R = sum([i for i in range(1, 2 * MATRIX_SIZE, 4)]) + \
             sum([i for i in range(4, 2 * MATRIX_SIZE, 4)])
class TestTDFMatrix(unittest.TestCase):
    def test_copy(self):
        n_matrix = MATRIX.copy()
        self.assertEqual(n_matrix, MATRIX)

        n_matrix.scale(2)
        self.assertNotEqual(n_matrix, MATRIX)

    def test_all_to_affine(self):
        MATRIX.all_to_affine()
        
        self.assertTrue(all([(g0.z == ONE) and (g1.z == ONE) for g0, g1 in MATRIX.M]))
        self.assertTrue(MATRIX.all_validate())

    def test_serialization(self):
        serialize(MATRIX, MATRIX_TEST_SERIALIZE_FILE)
        n_matrix = deserialize(MATRIX_TEST_SERIALIZE_FILE)
        
        MATRIX.all_to_affine()
        
        self.assertEqual(n_matrix, MATRIX)
        self.assertTrue(MATRIX.all_validate())
        self.assertTrue(n_matrix.all_validate())

    def test_dot(self):
        self.assertRaises(TDFError, MATRIX.dot, bitarray(1) * (MATRIX_SIZE + 1))
        
        hashed = MATRIX.dot(DOT_TEST).to_affine()
        self.assertEqual(hashed, GE(DOT_TEST_R).to_affine())

        short_dot = MATRIX.dot([0]).to_affine()
        self.assertEqual(short_dot, GE(1).to_affine())
    
    def test_scale(self):
        n_matrix = MATRIX.copy()
        n_matrix.scale(42)
        scaled_hash = n_matrix.dot(DOT_TEST).to_affine()
        self.assertEqual(scaled_hash, GE(DOT_TEST_R * 42).to_affine())

