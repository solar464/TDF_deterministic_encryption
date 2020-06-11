import owfe
from floodberry.floodberry_ed25519 import GE25519 as GE
from random import randint
"""
Incomplete implementation of Strong TDF (from smooth recyclable OWFE)
Section 4 of https://eprint.iacr.org/2018/872.pdf
"""

class IndexKey:
    def __init__(self, pp, a, CT):
        assert len(pp) == len(CT) and len(pp) == len(a): "n values inconsistent"
        self.pp = pp
        self.CT = CT
        self.a = a
        self.m = len(pp)

    @property
    def pp(self):
        return self.pp
    @property
    def a(self):
        return self.a
    @property
    def CT(self):
        return self.CT
    @property
    def m(self):
        return self.m

class TrapdoorKey:
    def __init__(self, pp, PP):
        self.pp = pp
        self.a = a
        self.P = P
        self.m = len(pp)

    @property
    def pp(self):
        return self.pp
    @property
    def a(self):
        return self.a
    @property
    def P(self):
        return self.P
    @property
    def m(self):
        return self.m

def Mir(pp, x, CT, a):
    bin_x = str_to_bin_list(x)
    n = len(a)
    M = [None for _ in range(n))]
    for i in range(n):
        b = D(pp, CT[i][bin_x[i]], x)
        if bin_x[i]:
            M[i] = (a[i] ^ b, b)
        else:
            M[i] = (b, a[i] ^ b)
    return M

def RSum(M):
    xor = lambda i,j: i^j
    a = [reduce(xor, v) for v in a]

def KG(m: int, lmbd: int = 254):
    limit = (1<<lmbd)
    pp = owfe.K(m, lmbd)
    P = randint(limit,size=(m,2))
    CT = [(owfe.E1(pp,j,0,P[j][0]), owfe.E1(pp,j,1,P[j][1])) for j in range(m)]

    a = randint(1, size=m)
    return IndexKey(pp, a, CT), TrapdoorKey(pp, a, P)

def F(ik: IndexKey, x):
    z = x #TODO: change z to erasure resilient encoding of x
    return (owfe.f(pp, z), Mir(pp, z, ik.CT, ik.a))

def F_inv(tk: TrapdoorKey, y: GE, M: list):
    assert RSum(M) == tk.a: "F_inv: RSum(M) != a"
    z_prime = [None for _ in range(tk.m)]
    for i in range(tk.m):
        b0 = owfe.E2(tk.pp, y, i, 0, tk.P[i][0])
        b1 = owfe.E2(tk.pp, y, i, 1, tk.P[i][1])
        if M[i] == [b0, not b1]:
            z_prime[i] = 1
        elif M[i] == [not b0, b1]:
            z_prime[i] = 0
    
    x = z_prime #TODO: change x to erasure resilient decoding of z_prime
    if F(ik, x) == u:
        return x
    return None
    



    
