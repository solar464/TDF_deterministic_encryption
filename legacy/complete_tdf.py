from floodberry.floodberry_ed25519 import GE25519 as GE
from tdf_strucs import TDFError, TDFMatrix, IndexKey, TrapdoorKey, TDFCipherText, TDFCodec
from utils import str_to_bitarr, int_lst_to_bitarr

from random import randint
from bitarray import bitarray
from array import array
import pickle

G1 = GE(1).to_affine()

class CTDFCipherText(TDFCipherText):
    def __init__(self, gc: GE, hc_list: bitarray):
        assert gc.validate(), "Ciphertext hash invalid."
        self._gc = gc
        self._b_prime = hc_list

    def __eq__(self, other):
        return all([
            self.gc == other.gc,
            self.b_prime == other.b_prime
        ])

class CTDFCodec(TDFCodec):
    def __init__(self, max_len: int, lmbd: int = 254):
        self._ik, self._tk = self.KG(max_len, lmbd)

    #F()
    def encode(self, msg, c:int = 8):
        # (msg) will be converted to bitarray
        # c = character size in bits
        
        if type(msg) == str:
            msg = str_to_bitarr(msg)
        elif type(msg) == list or type(msg) == array:
            msg = int_lst_to_bitarr(msg, c)

        self.encode_validate(msg, c)
        
        hashes = [
            self.ik.M[i].dot(msg).to_affine() 
            for i in range(len(msg))
        ]
        self.encode_hashes = hashes

        pad = bitarray([
            self.pad_bit(self.ik.M[i].dot(msg).to_affine()) 
            for i in range(len(msg))
        ], endian='little')
        #print("Message   : {}".format(msg))
        #print("Encode pad: {}".format(pad))
        #print("CipherText: {}".format(msg^pad))
        return CTDFCipherText(
            self.ik.base_M.dot(msg).to_affine(), 
            msg ^ pad
        )
    
    #F_inv()
    def decode(self, u: CTDFCipherText):
        self.decode_validate(u)

        hashes = [
            u.gc.copy().scale(self.tk.r[i]).to_affine() 
            for i in range(u.length)
        ]
        self.decode_hashes = hashes
        
        pad = bitarray([
            self.pad_bit(u.gc.copy().scale(self.tk.r[i]).to_affine()) 
            for i in range(u.length)
        ], endian='little')
        #print("Ciphertext: {}".format(u.b_prime))
        #print("Decode pad: {}".format(pad))
        return u.b_prime ^ pad 
    
    def encode_validate(self, msg, c: int):
        if len(msg) > self.max_len:
            raise TDFError("Encode: message is length {}, can only encode {} bits of erasure code".format(len(msg), self.max_len))
    
    def decode_validate(self, u: CTDFCipherText):
        if not self._tk:
            raise TDFError("Decode: this codec is a public key and does not have access to the required trapdoors to decode cipher texts")
        if not u.gc.validate():
            raise TDFError("Decode: invalid cipher text due to invalid group element.")
        if u.length > self.max_len:
            raise("Decode: cipher text is too long to decode, can only decode maximum of {} bits".format(self.max_len))
    
    def pad_bit(self, h: GE):
        #returns one bit of the pad for encode
        #return h.HC()
        # alternate method involving bit comparison between (h) and (h + g),
        #   start from LSB and go up until first differing pair of bits
        h.to_affine()
        x = h.x_int
        x1 = h.copy().add(G1).to_affine().x_int
        
        for _ in range(255):
            if (x & 1) != (x1 & 1):
                return (x & 1)
            x >>= 1
            x1 >>= 1
        
        #should never reach this point
        print("The points hash: {} \nhash + g: {} are identical?".format(h.sub(G1).to_affine(), h.add(G1).to_affine()))
        
        return 0
        
    def KG(self, m: int, lmbd: int = 254):
        print("CTDF: Generating Keys")
        limit = (1<<lmbd)
        base_M = TDFMatrix(m).init_random(lmbd)
        r = [randint(0, limit) for i in range(m)]
        M = [base_M.copy().scale(r[i]) for i in range(m)]

        print("CTDF: Finished generating {} keys".format(m))
        return IndexKey(base_M, M), TrapdoorKey(base_M, r)
    
    def KG_ls(self, m: int, lmbd: int = 254):
        limit = (1<<lmbd)
        base_M = TDFMatrix().init_random(lmbd)
        r = [randint(0, limit) for i in range(m)]

        M = [base_M.copy().scale(r[i]) for i in range(m)]

        return IndexKey(base_M, M)

"""
ctdf = CTDFCodec(max_len=24)

x = [0,1,2]
u = ctdf.encode(x, c=8)
result = ctdf.decode(u)
"""
