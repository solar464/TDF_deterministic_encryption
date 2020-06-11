from reedsolomon.reedsolo import RSCodec, find_prime_polys, ReedSolomonError
from utils import chunk, lst_to_int, int_lst_to_bitarr, str_to_int_lst

from bitarray import bitarray


#binary erasure code
#encodes by using reed solomon and then duplicating each bit
class BECError(Exception):
    pass

class BECCodec:
    def __init__(self, c: int = 8, nsym: int = 10, t: int = 8):
        if c <= 2:
            raise BECError("BECCodec, cannot make RSCodec with c_exp = {}".format(c))
        self._c = c         #character bit length
        self._nsym = nsym   #padding per block of 2**c - 1 characters
        self._t = t         #repetition per bit

        nsize = (1 << c) - 1
        c_exp = c
        prim_poly = find_prime_polys(c_exp=c_exp, single=True)
        
        self._codec = RSCodec(nsym=nsym, nsize=nsize, c_exp=c_exp, prim=prim_poly)

    def encode(self, msg): #msg should be list of int or string
        if isinstance(msg, str):
            msg = str_to_int_lst(msg, self.c)
        encoded = self.codec.encode(msg)
        #print("encoded: " + str(encoded))
        bits = int_lst_to_bitarr(encoded, self.c)
        #print("bits: " + str(bits))
        a = bitarray(endian='little')
        for i in bits:
            a.extend([i]*self.t)
        return a

    def decode(self, received):
        rs_bits = self.remove_repeats(received)
        rs_code = [0] * (len(rs_bits) // self.c)
        erase_pos = []
        for idx, char_lst in enumerate(chunk(rs_bits, self.c)):
            if None in char_lst:
                erase_pos.append(idx)
            else:
                rs_code[idx] = lst_to_int(char_lst)
        
        raw_none = received.count(None) if isinstance(received, list) else 0
        contract_none = rs_bits.count(None)
        erased_count = len(erase_pos)
#        print("Decode: Raw None = " + str(raw_none) + " / " + str(len(received)) + " \t Contracted None = " + str(contract_none) + " / " + str(len(rs_bits)) + " \t Erased characters = " + str(erased_count) + " / " + str(len(rs_code)) + " = " + "{0:.3f}".format(erased_count/len(rs_code)))
        
        return self._codec.decode(rs_code, erase_pos=erase_pos, only_erasures=True)

    def remove_repeats(self, lst):
        rs_bits = []
        for bit_lst in chunk(lst, self.t):
            if 1 in bit_lst and 0 in bit_lst:
                raise BECError('Both 0 and 1 found in chunk of repeated bits')
            if 1 in bit_lst:
                rs_bits.append(1)
            elif 0 in bit_lst:
                rs_bits.append(0)
            else:
                rs_bits.append(None)
        return rs_bits
    
    @property
    def c(self):
        return self._c
    @property
    def nsym(self):
        return self._nsym
    @property
    def t(self):
        return self._t
    @property
    def codec(self):
        return self._codec
        
