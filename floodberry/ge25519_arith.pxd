# ge25519_arith.pxd

from libc.stdint cimport uint64_t

cdef extern from "ge25519_pt_arith.h":
    ctypedef uint64_t bignum25519[5]
    ctypedef uint64_t bignum256modm[5]
    ctypedef struct ge25519:
        bignum25519 x, y, z, t

    void ge25519_scalarmult(ge25519* r, const ge25519* p, const bignum256modm scalar)
    void ge25519_scalarmult_base(ge25519* r, const bignum256modm scalar)
    void ge25519_add(ge25519* r, ge25519* p, ge25519* q)
    void ge25519_double(ge25519* r, ge25519* p)
    
    void ge25519_to_affine(ge25519* r)
    bint ge25519_eq(const ge25519* a, const ge25519* b)
    bint ge25519_validate(const ge25519* a)
    void ge25519_copy(ge25519* r, const ge25519* p)

    void ge25519_pack(unsigned char r[32], ge25519* p)
    void ge25519_unpack_vartime(ge25519* p, const unsigned char r[32])
    
    void expand256_modm(bignum256modm out, unsigned char*, size_t length)
    void expand_raw256_modm(bignum256modm out, unsigned char*)
