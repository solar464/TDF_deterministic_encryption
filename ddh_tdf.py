from __future__ import annotations
from array import array
from bitarray import bitarray # type: ignore
from random import randint
from typing import List, Tuple, Sequence, Union
import pickle

from floodberry.floodberry_ed25519 import GE25519 as GE # type: ignore 

"""
Some basic data structures for use in TDF encryption
"""
class TDFError(Exception):
    pass

class TDFVector:
    def __init__(self, m: int, lmbd: int = 254):
        self._M = [None] * m
 
    def init_random(self, lmbd: int = 254) -> TDFVector:
        limit = (1<<lmbd)
        for i in range(self.length):
            self.M[i] = GE(randint(1, limit))
        assert self.all_validate(), "TDFVector contains invalid points"
        return self

    def copy(self) -> TDFVector:
        newVector = TDFVector(self.length)
        for i in range(self.length):
            newVector.M[i] = self.M[i].copy()
        return newVector

    def scale(self, r: int) -> TDFVector:
        for g in self.M:
            g.scale(r)
        return self

    def set(self, i: int, g: GE) -> TDFVector:
        self.M[i] = g
        return self

    def dot(self, x: Sequence[Union[int, str, bool]]) -> GE:
        # x: bitarray, binary list, binary string, etc.
        #assert len(x) <= self.size, "dot: x is too long, len(x) = " + str(len(x)) + " > " + str(self.size)
        if len(x) > self.length:
            raise TDFError('dot: x is too long, len(x) = {} > {}'.format(len(x),self.length))
        a = GE(0)
        for i in range(1, len(x)):
            if x[i]:
                a.add(self.M[i])
        return a
    
    def all_to_affine(self) -> TDFVector:
        for g in self.M:
            g.to_affine()
        return self

    def all_validate(self) -> bool:
        return all([g.validate() for g in self.M])

    @property
    def M(self) -> List[GE]:
        return self._M
    @property
    def length(self) -> int:
        return len(self.M)

    def __eq__(self, other) -> bool:
        if isinstance(other, TDFVector):
            return self.M == other.M 
        return NotImplemented

class DDH_TDF_CipherText:
    def __init__(self, gc: GE, hc_list: bitarray):
        assert gc.validate(), "Ciphertext hash invalid."
        self._gc = gc
        self._b_prime = hc_list

    @property
    def gc(self) -> GE:
        return self._gc
    @property
    def b_prime(self) -> bitarray:
        return self._b_prime
    @property
    def length(self) -> int:
        return len(self.b_prime)
    """
    def serialize(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def deserialize(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    """
    def all_to_affine(self) -> DDH_TDF_CipherText:
        self.gc.to_affine()
        return self

    def __eq__(self, other) -> bool:
        if isinstance(other, DDH_TDF_CipherText):
            return all([
                self.gc == other.gc,
                self.b_prime == other.b_prime
            ])
        return NotImplemented

class DDH_TDF_IndexKey:
    def __init__(self, base_M: TDFVector, M: List[TDFVector]):
        for m in M:
            assert base_M.length == m.length, "IndexKey, vector sizes inconsistent"
        self._base_M = base_M
        self._M = M

    #F()
    def encode(self, msg: bytes) -> DDH_TDF_CipherText:
        # (msg) will be converted to bitarray
        msg_bits = bitarray(endian="little")
        msg_bits.frombytes(msg)
        self.encode_validate(msg_bits)
    
        """
        #for debugging
        hashes = [ 
            self.M[i].dot(msg_bits).to_affine() 
            for i in range(len(msg_bits))
        ]
        self.encode_hashes = hashes
        """

        pad = bitarray([
            self.M[i].dot(msg_bits).HC() 
            for i in range(len(msg_bits))
        ], endian='little')
        #print("Message   : {}".format(msg))
        #print("Encode pad: {}".format(pad))
        #print("CipherText: {}".format(msg^pad))
        return DDH_TDF_CipherText(
            self.base_M.dot(msg_bits).to_affine(), 
            msg_bits ^ pad 
        )
    
    def encode_validate(self, msg) -> None:
        if len(msg) > self.length:
            raise TDFError("Encode: message is length {}, can only encode {} bits of erasure code".format(len(msg), self.length))

    def all_to_affine(self) -> DDH_TDF_IndexKey:
        self.base_M.all_to_affine()
        for m in self.M:
            m.all_to_affine()
        return self
    
    @property
    def base_M(self) -> TDFVector:
        return self._base_M
    @property
    def M(self) -> List[TDFVector]:
        return self._M
    @property
    def length(self) -> int:
        return self._base_M.length

    def __eq__(self, other) -> bool:
        if isinstance(other, DDH_TDF_IndexKey):
            return all([
                self.base_M == other.base_M,
                self.M == other.M,
            ])
        return NotImplemented

class DDH_TDF_TrapdoorKey:
    def __init__(self, r: List[int]):
        self._r = r

    #F_inv()
    def decode(self, u: DDH_TDF_CipherText) -> bytes:
        self.decode_validate(u)

        """
        #for debugging
        hashes = [
            u.gc.copy().scale(self.r[i]).to_affine()
            for i in range(u.length)
        ]
        self.decode_hashes = hashes
        """

        pad = bitarray([
            u.gc.copy().scale(self.r[i]).HC()
            for i in range(u.length)
        ], endian='little')
        #print("Ciphertext: {}".format(u.b_prime))
        #print("Decode pad: {}".format(pad))
        return (u.b_prime ^ pad).tobytes()

    def decode_validate(self, u: DDH_TDF_CipherText) -> None:
        if not u.gc.validate():
            raise TDFError("Decode: invalid cipher text due to invalid group element.")
        if u.length > self.length:
            raise TDFError("Decode: cipher text is too long to decode, can only decode maximum of {} bits".format(self.length))

    def all_to_affine(self) -> DDH_TDF_TrapdoorKey:   
        #DDHTrapdoor contains no ed25519 points
        return self

    @property
    def r(self) -> List[int]:
        return self._r
    @property
    def length(self) -> int:
        return len(self._r)

    def __eq__(self, other) -> bool:
        if isinstance(other, DDH_TDF_TrapdoorKey):
            return self.r == other.r
        return NotImplemented

def KG(length: int, lmbd: int = 254) -> Tuple[DDH_TDF_IndexKey, DDH_TDF_TrapdoorKey]:
    print("DDH_TDF: Generating Keys")
    limit = (1<<lmbd)
    base_M = TDFVector(length).init_random(lmbd)
    r = [randint(1, limit) for i in range(length)]
    M = [base_M.copy().scale(r[i]) for i in range(length)]

    print("DDH_TDF: Finished generating {} keys".format(length))
    return DDH_TDF_IndexKey(base_M, M), DDH_TDF_TrapdoorKey(r)

def KG_ls(length: int, lmbd: int = 254) -> DDH_TDF_IndexKey:
    limit = (1<<lmbd)
    base_M = TDFVector(length).init_random(lmbd)
    r = [randint(1, limit) for i in range(length)]
    M = [base_M.copy().scale(r[i]) for i in range(length)]
    for i in range(length):
        M[i].set(i, GE(randint(1, limit)))
    return DDH_TDF_IndexKey(base_M, M)

