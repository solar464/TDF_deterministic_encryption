import unittest
import BEC
import reedsolomon
from reedsolomon.reedsolo import ReedSolomonError
from bitarray import bitarray
from array import array

class TestBEC(unittest.TestCase):
    def setUp(self):
        self.c = 4
        self.nsym = 1
        self.t = 2
        self.bec = BEC.BECCodec(c=self.c,nsym=self.nsym,t=self.t)
        self.message = 'hi'
        self.message_int_lst = array('i', BEC.str_to_int_lst(self.message, self.c))
        self.ct = bitarray('0000001100111100110000110011110011000000')
        
    def test_encode(self):
        self.assertEqual(self.bec.encode(self.message), self.ct)

    def test_decode_no_erasures(self):
        self.assertEqual(self.bec.decode(self.ct), self.message_int_lst)
        self.assertEqual(self.bec.decode(list(self.ct)), self.message_int_lst)
    
    def test_decode_tolerable_erasure(self):
        ct = [None] * len(self.ct)
        remaining = list(range(0,len(ct),self.t))[self.nsym * self.c:]
        for i in remaining:
            ct[i] = self.ct[i]

        self.assertEqual(self.bec.decode(ct), self.message_int_lst)

    def test_fail_decode_many_erasures(self):
        ct = list(self.ct)
        for i in range(self.t * self.c * (self.nsym + 1)):
            ct[i] = None
        with self.assertRaises(ReedSolomonError) as context:
            self.bec.decode(ct)
        self.assertTrue('Too many erasures to correct' in str(context.exception))
        
