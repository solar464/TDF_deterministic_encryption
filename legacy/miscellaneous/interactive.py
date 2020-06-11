from floodberry_ed25519 import *

"""
Initializes an interactive python session with useful values.
For manual testing of floodberry_ed25519
"""

ge = GE25519
L = (1<<252) + 2774231777737235353585193779088364849
L2 = (1<<253) - 5548463555474470707170387558176729699
M = (1<<255) - 19

one = ge(1)
two = ge(2)

X = [0x00062d608f25d51a,0x000412a4b4f6592a,0x00075b7171a4b31d,0x0001ff60527118fe,0x000216936d3cd6e5]
Y = [0x0006666666666658,0x0004cccccccccccc,0x0001999999999999,0x0003333333333333,0x0006666666666666]
Z = 1
T = [0x00068ab3a5b7dda3,0x00000eea2a5eadbb,0x0002af8df483c27e,0x000332b375274732,0x00067875f0fd78b7]

X = bn_to_int(X)
Y = bn_to_int(Y)
T = bn_to_int(T)


def scale(a, e):
    total = ge(0)
    while e > 0:
        if (e&1):
            total.add(a)
        a.double()
        e >>= 1
    return total
