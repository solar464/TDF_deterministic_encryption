from floodberry.floodberry_ed25519 import GE25519 as GE
from random import randint

"""
Draft implementation of Smooth Recyclable OWFE (from CDH).
From section 3 of https://eprint.iacr.org/2018/872.pdf
"""

def str_to_bin_list(x) -> list:
    binstr = ''.join(['{0:08b}'.format(ord(c)) for c in x])
    return [True if i == '1' else False for i in binstr]
    
def K(n: int, lmbd: int = 254) -> list:
    limit = 1 << lmbd
    return [(GE(randint(0, limit)), GE(randint(0, limit))) for i in range(n)]

def f(PP, x) -> GE:
    y: GE = GE(0)
    bin_x = str_to_bin_list(x)
    for i in range(len(bin_x)):
        y.add(PP[i][bin_x[i]])
    return y

def E1(PP, i, b, rho) -> list:
    n = len(PP)
    ct = [None for i in range(n)]
    for j in range(n):
        if i == j:
            if b:
                ct[j] = (GE(0), GE.copy(PP[j][1]).scale(rho))
            else:
                ct[j] = (GE.copy(PP[j][0]).scale(rho), GE(0))
        else:
            ct[j] = (GE.copy(PP[j][0]).scale(rho), GE.copy(PP[j][1]).scale(rho))
    
    return ct

def E2(PP, y, i, b, rho) -> bool:
    return GE.copy(y).scale(rho).HC()

def D(PP, ct, x) -> bool:
    return f(ct, x).HC()
           
class OWFE:
    def __init__(self, n, lmbd=253):
        pass

def test_owfe(x):
    bin_x = str_to_bin_list(x)
    n = len(bin_x)
    pp = K(n)
    rho = randint(0,1<<253)
    y: GE = f(pp, x)
    print("y: " + str(y))
    for i in range(n):
        b = bin_x[i]
        ct = E1(pp,i,b,rho)
        correct = E2(pp,y,i,b,rho) 
        result = D(pp,ct,x)
        if result != correct:
            print("You fucked up the OWFE implementation")
            break
    else:
        print("Everything seems fine for OWFE")
