from BEC import *
import unittest
from random import randint

def mock_decoder(lst):
    return [i if randint(0,100) > 75 else None for i in lst]

def test(c: int = 8, c1: int = 8, t: int = 8, i = 100, a=b'Hello World!'):
    rs = BECCodec(c,c1,t)
    successful = 0
    b = rs.encode(a)

    for _ in range(i):
        lossy_b = mock_decoder(b)
        try:
            if a == rs.decode(lossy_b):
                successful += 1
            else:
                print("decoded incorrectly?")
        except Exception as e:
            continue

    return successful / i

