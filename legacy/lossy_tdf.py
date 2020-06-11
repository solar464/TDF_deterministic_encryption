from floodberry.floodberry_ed25519 import GE25519 as GE
from BEC import BECCodec
from tdf_strucs import TDFError, TDFMatrix, IndexKey, TrapdoorKey, TDFCipherText, TDFCodec

from random import randint
from bitarray import bitarray
import pickle

"""
Implementation of Lossy TDF from DDH (linear image size)
Section 6 of https://eprint.iacr.org/2018/872.pdf
"""
"""
#for deriving padding number from desired expansion factor (c1)
nsym = int((1-1/c1)*nsize)
if msg_len * c1 < nsize:
    self._nsym = (c1 - 1) * msg_len
"""
class LTDFCipherText(TDFCipherText):
    def __init__(self, gc: GE, hc_list: bitarray, c: int, nsym: int, t: int):
        self._gc = gc
        self._b_prime = hc_list
        
        #for constructing the BECCodec
        self._c = c
        self._nsym = nsym
        self._t = t
    
    def get_BECCodec(self):
        return BECCodec(c=self._c, nsym=self._nsym, t=self._t)
    
    def __eq__(self, other):
        return all([
            self.gc == other.gc,
            self.b_prime == other.b_prime,

            self._c == other._c,
            self._nsym == other._nsym,
            self._t == other._t
        ])

class LTDFCodec(TDFCodec):
    def __init__(self, max_len: int, lmbd: int = 254):
        self._ik, self._tk = self.KG(max_len, lmbd)

    def encode(self, msg, c: int = 8, nsym: int = -1, t: int = 10):
        # set erasure correction bits so expansion factor is 2
        if nsym < 0:
            nsym = min(len(msg), 2 << (c - 1))

        return self.encode(BECCodec(c=c, nsym=nsym, t=t))

    #F()
    def encode(self, msg, bec: BECCodec):
        z = bec.encode(msg)
        
        self.encode_validate(msg, z, bec)
        
        return LTDFCipherText(
            self.ik.base_M.dot(z), 
            bitarray([m.dot(z).HC() for m in self.ik.M[:len(z)]]),
            c = bec.c,
            nsym = bec.nsym,
            t = bec.t
        )
    
    #F_inv()
    def decode(self, u: LTDFCipherText):
        self.decode_validate(u)
        z_prime = [None for _ in range(u.length)]

        for i in range(u.length):
            if u.b_prime[i] != u.gc.copy().scale(self.tk.r[i]).HC():
                z_prime[i] = self.tk.b[i]
        
        return u.get_BECCodec().decode(z_prime) 
    
    def encode_validate(self, msg, z, bec: BECCodec):
        #assert len(z) <= self.max_len, \
        if len(z) > self.max_len:
            raise TDFError("Encode: message is too long, can only encode {} bits of erasure code".format(self.max_len))
    
    def decode_validate(self, u: LTDFCipherText):
        #assert self._tk, \
        if not self._tk:
            raise TDFError("Decode: this codec is a public key and does not have access to the required trapdoors to decode cipher texts")
        #assert u.gc.validate(), \
        if not u.gc.validate():
            raise TDFError("Decode: invalid cipher text due to invalid group element.")
        #assert u.length <= self.max_len, \
        if u.length > self.max_len:
            raise("Decode: cipher text is too long to decode, can only decode maximum of {} bits".format(self.max_len))
    
    def KG(self, m: int, lmbd: int = 254):
        print("LTDF: Generating Keys")
        limit = (1<<lmbd)
        base_M = TDFMatrix(m).init_random(lmbd)
        r = [randint(0, limit) for i in range(m)]
        b = [randint(0,1) for i in range(m)]
        g = [GE(randint(0, limit)) for i in range(m)]

        M = [base_M.copy().scale(r[i]).set(i, b[i], g[i].copy()) for i in range(m)]

        print("LTDF: Finished generating {} keys".format(m))
        return IndexKey(base_M, M), TrapdoorKey(base_M, r, b, g)
    
    def KG_ls(self, m: int, lmbd: int = 254):
        limit = (1<<lmbd)
        base_M = TDFMatrix().init_random(lmbd)
        r = [randint(0, limit) for i in range(m)]

        M = [base_M.copy().scale(r[i]) for i in range(m)]

        return IndexKey(base_M, M)
"""
ltdf = LTDFCodec(msg_len = 3, c = 4, t=10, c1=2)

x = [0,1,2]
u = ltdf.encode(x)
result = ltdf.decode(u)
"""
