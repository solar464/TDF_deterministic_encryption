from floodberry.floodberry_ed25519 import GE25519 as GE
from random import randint
from bitarray import bitarray
import pickle

"""
Some basic data structures for use in TDF encryption
"""
class TDFError(Exception):
    pass

class TDFMatrix:
    def __init__(self, m: int, lmbd: int = 254):
        self._M = [[None,None] for _ in range(m)]
 
    def init_random(self, lmbd: int = 254):
        limit = (1<<lmbd)
        for i in range(self.size):
            self.M[i][0] = GE(randint(0, limit))
            self.M[i][1] = GE(randint(0, limit))
        assert self.all_validate(), "TDFMatrix contains invalid points"
        return self

    def copy(self):
        newMatrix = TDFMatrix(self.size)
        for i in range(self.size):
            newMatrix.M[i][0] = self.M[i][0].copy()
            newMatrix.M[i][1] = self.M[i][1].copy()
        return newMatrix

    def scale(self, r: int):
        for ge0, ge1 in self.M:
            ge0.scale(r)
            ge1.scale(r)
        return self

    def set(self, i: int, b: int, g: GE):
        self.M[i][b] = g
        return self

    def dot(self, x):
        # x: bitarray, binary list, binary string, etc.
        #assert len(x) <= self.size, "dot: x is too long, len(x) = " + str(len(x)) + " > " + str(self.size)
        if len(x) > self.size:
            raise TDFError('dot: x is too long, len(x) = {} > {}'.format(len(x),self.size))
        a: GE = self.M[0][x[0]].copy()
        for i in range(1, len(x)):
            a.add(self.M[i][x[i]])
        return a
    
    def all_to_affine(self):
        for g0, g1 in self.M:
            g0.to_affine()
            g1.to_affine()

    def all_validate(self):
        return all([g0.validate() and g1.validate() for g0, g1 in self.M])

    @property
    def M(self):
        return self._M
    @property
    def size(self):
        return len(self.M)

    def __eq__(self, other):
        return self.M == other.M 

class IndexKey:
    def __init__(self, base_M, M):
        for m in M:
            assert base_M.size == m.size, "IndexKey, matrix sizes inconsistent"
        self._base_M = base_M
        self._M = M

    def all_to_affine(self):
        self.base_M.all_to_affine()
        for m in self.M:
            m.all_to_affine()
        return self
    
    @property
    def base_M(self):
        return self._base_M
    @property
    def M(self):
        return self._M
    @property
    def m(self):
        return self._base_M.size

    def __eq__(self, other):
        return all([
            self.base_M == other.base_M,
            self.M == other.M,
            self.m == other.m
        ])

class TrapdoorKey:
    def __init__(self, M, r, b=None, g=None):
        m = M.size
        assert m == len(r), "TrapdoorKey, {} matrices and {} secret scalars. Should be equal.".format(m, len(r))
        if b and g:
            assert m == len(b) and  m == len(g), "TrapdoorKey, b and g lengths ({}, {}) inconsistent with matrix number: {}.".format(len(b), len(g), m)
        self._base_M = M
        self._r = r
        self._b = b
        self._g = g

    def all_to_affine(self):   
        self.base_M.all_to_affine()
        if self.g:
            for g in self.g:
                g.to_affine()
        return self

    @property
    def base_M(self):
        return self._base_M
    @property
    def r(self):
        return self._r
    @property
    def b(self):
        return self._b
    @property
    def g(self):
        return self._g
    @property
    def m(self):
        return self._base_M.size

    def __eq__(self, other):
        return all([
            self.base_M == other.base_M,
            self.r == other.r,
            self.b == other.b,
            self.g == other.g,
            self.m == other.m
        ])

class TDFCipherText:
    @property
    def gc(self):
        return self._gc
    @property
    def b_prime(self):
        return self._b_prime
    @property
    def length(self):
        return len(self.b_prime)

    def serialize(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def deserialize(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    def all_to_affine(self):
        self.gc.to_affine()
        return self


class TDFCodec:
    #F()
    def encode(self, msg):
        pass

    #F_inv()
    def decode(self, u: TDFCipherText):
        pass

    def KG(self, m: int, lmbd: int = 254):
        pass

    def KG_ls(self, m: int, lmbd: int = 254):
        pass

    def serialize(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def deserialize(filename):
        with open(filename, 'rb') as f:
            codec = pickle.load(f)
        return codec

    def all_to_affine(self):
        self.ik.all_to_affine()
        self.tk.all_to_affine()
        return self

    @property
    def ik(self):
        return self._ik
    @property
    def tk(self):
        return self._tk
    @property
    def max_len(self):
        return self.ik.base_M.size

    def __eq__(self, other):
        return all([
            self.ik == other.ik,
            self.tk == other.tk
        ])
