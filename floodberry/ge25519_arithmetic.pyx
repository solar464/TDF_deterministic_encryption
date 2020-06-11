# distutils: sources = ge25519_pt_arith.c
# distutils: include_dirs = donna

from ge25519_arith cimport *
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.stdint cimport uint64_t
from bitarray import bitarray

LAST_56 = (1<<56) - 1
# for converting to bignum256modm for exponents
cdef int_to_modm(uint64_t r[5], x):
    r[0] = x & LAST_56; x >>= 56
    r[1] = x & LAST_56; x >>= 56
    r[2] = x & LAST_56; x >>= 56
    r[3] = x & LAST_56; x >>= 56
    r[4] = x & LAST_56;

# for converting bignum25519 attributes of ge25519
def bn_to_int(x):
    r = x[4]; r <<= 51
    r |= x[3]; r <<= 51
    r |= x[2]; r <<= 51
    r |= x[1]; r <<= 51
    return r | x[0]

cdef uint64_t* expand_modm(x: int):
    cdef uint64_t a[5]
    expand256_modm(a, x.to_bytes(32, "little"), 32)
    print(a)
    return a

cdef uint64_t* expandraw_modm(x: int):
    cdef uint64_t a[5]
    expand_raw256_modm(a, x.to_bytes(32, "little"))
    print(a)
    return a
    
def naive_scale(e: int, a: GE25519):
    base = a.copy()
    total = GE25519(0)
    while e > 0:
        if (e&1):
            total.add(base)
        base.double()
        e >>= 1
    return total
    

cdef class GE25519(object):
    cdef ge25519* _ge

    def __cinit__(self):
        self._ge = <ge25519*> PyMem_Malloc(sizeof(ge25519))
        if not self._ge:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self._ge)
    
    def __init__(self, x: int = -1):
        #cdef uint64_t r[5]
        #int_to_modm(r,x)
        if x < 0:
            return 

        cdef bignum256modm r
        expand_raw256_modm(r, x.to_bytes(32, "little"))
        ge25519_scalarmult_base(self._ge, r) 
    
    def scale(self, x: int):
        #cdef uint64_t r[5]
        #int_to_modm(r,x)
        #ge25519_scalarmult(self._ge, self._ge, r)
        cdef bignum256modm r
        expand_raw256_modm(r, x.to_bytes(32, "little"))
        ge25519_scalarmult(self._ge, self._ge, r) 
        return self
    
    def add(self, q: GE25519):
        ge25519_add(self._ge, self._ge, q._ge)
        return self

    def double(self):
        ge25519_double(self._ge, self._ge)
        return self

    def to_affine(self):
        ge25519_to_affine(self._ge)
        return self
    
    def HC(self):
        self.to_affine()
        return self.x[0] & 1

    def validate(self):
        return ge25519_validate(self._ge)
    
    def copy(self):
        new_point: GE25519 = GE25519()
        ge25519_copy(new_point._ge, self._ge)
        return new_point

    def pack(self):
        cdef bytes py_bytes = b'0'*32
        cdef unsigned char* c_string = py_bytes
        ge25519_pack(c_string, self._ge)
        return py_bytes
    
    def unpack(self, packed: bytes):
        assert len(packed) == 32, "GE25519.unpack, input = {} || length = {} || must unpack from 32 bytes".format(packed, len(packed))
        #cdef bytes py_bytes = state.encode()
        cdef unsigned char* c_string = packed
        ge25519_unpack_vartime(self._ge, c_string)
        return self
        
    def __eq__(self, other: GE25519):
        return ge25519_eq(self._ge, other._ge)

    def __repr__(self):
        return "x: " + str(bn_to_int(self._ge.x)) + \
             "\ny: " + str(bn_to_int(self._ge.y)) + \
             "\nz: " + str(bn_to_int(self._ge.z)) + \
             "\nt: " + str(bn_to_int(self._ge.t)) + "\n"
    
    def __str__(self):
        return self.__repr__()
    
    def __getstate__(self):
        return list(self.pack())

    def __setstate__(self, state):
        self.unpack(bytes(state))

    @property
    def x(self):
        return self._ge.x
    @property
    def y(self):
        return self._ge.y
    @property
    def z(self):
        return self._ge.z
    @property
    def t(self):
        return self._ge.t

    @property
    def x_int(self):
        return bn_to_int(self._ge.x)
