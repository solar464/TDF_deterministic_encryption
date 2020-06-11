import unittest
import floodberry
from floodberry.floodberry_ed25519 import GE25519 as GE

import pickle

SERIALIZE_TEST_FILE = "tests/test_ge.p"
SERIALIZE_LIST_TEST_FILE = "tests/test_ge_list.p"

packed42 = b'\xce\x1a2\x99N\x83\\\x19>+\xf39\t\xf4Cs\xae,\xf9M\xde\xf0\xfd\x92 5\xc4\x83g\x067\xc2'
ge42 = GE(42).to_affine()

ge42x = [638129450090601, 1092992485173610, 659239496376681, 1398765529464492, 1649159199051745]
ge42y = [1270273507728078, 324623919465259, 2221781109510096, 721595290644262, 1164865569307715]
ge42z = [1, 0, 0, 0, 0]
ge42t = [621704001636999, 755815915372815, 259964580607406, 1557714783488804, 1367295035199813]

class TestGE(unittest.TestCase):

    def test_accessors(self):
        self.assertEqual(ge42.x, ge42x)
        self.assertEqual(ge42.y, ge42y)
        self.assertEqual(ge42.z, ge42z)
        self.assertEqual(ge42.t, ge42t)
        self.assertEqual(ge42.HC(), ge42x[0] & 1)

    def test_scale(self):
        self.assertEqual(ge42, GE(6).scale(7).to_affine())

    def test_add(self):
        self.assertEqual(ge42, GE(20).add(GE(22)).to_affine())

    def test_double(self):
        self.assertEqual(ge42, GE(21).double().to_affine())

    def test_validate(self):
        self.assertTrue(ge42.validate())
        bad_ge = b'\xce\x1a2XXXXXXX\xf39\t\xf4Cs\xae,\xf9M\xde\xf0\xfd\x92 5\xc4\x83g\x067\xc2'

        self.assertFalse(GE().unpack(bad_ge).validate())

    def test_copy(self):
        ge_old = GE(42)
        ge_new = ge_old.copy().to_affine()

        self.assertNotEqual(ge_old, ge_new)
        self.assertEqual(ge_new, ge42)

    def test_packing(self):
        self.assertEqual(GE(42).pack(), packed42)
        self.assertEqual(GE().unpack(packed42), ge42)

    def test_serialization(self):
        with open(SERIALIZE_TEST_FILE, "wb") as f:
            pickle.dump(ge42, f)
        with open(SERIALIZE_TEST_FILE, "rb") as f:
            self.assertEqual(pickle.load(f), ge42)

    def test_serialization_list(self):
        x = [GE(3).to_affine(), GE(4).to_affine(), GE(5).to_affine()]
        with open(SERIALIZE_LIST_TEST_FILE, "wb") as f:
            pickle.dump(x, f)
        with open(SERIALIZE_LIST_TEST_FILE, "rb") as f:
            self.assertEqual(pickle.load(f), x)
