import sys
sys.path.append("..")

from floodberry import floodberry_ed25519
import timeit

from benchmark_constants import ED_REPEAT as REPEAT_NUM
"""
Benchmarks the elliptic curve arithmetic.
"""


#scale base point
setup = "from floodberry_ed25519 import GE25519 as ge; from random import randint"
statement = "a = ge(randint(0, 1<<253))"
time = timeit.timeit(statement, setup, number=REPEAT_NUM)
print("Scaling hardcoded base point g {} times".format(REPEAT_NUM))
print(time)

#scale any point
setup = "from floodberry_ed25519 import GE25519 as ge; from random import randint; a = ge(1)"
statement = "a.scale(randint(0, 1<<253))"
time = timeit.timeit(statement, setup, number=REPEAT_NUM)
print("Scaling arbitrary point {} times".format(REPEAT_NUM))
print(time)

#scale any point naively
setup = "from floodberry_ed25519 import GE25519 as ge, naive_scale; from random import randint; a = ge(1)"
statement = "naive_scale(randint(0, 1<<253), a)"
time = timeit.timeit(statement, setup, number=REPEAT_NUM)
print("Scaling through double and add {} times".format(REPEAT_NUM))
print(time)

"""
0.09327135048806667
0.3140125358477235
0.6910017551854253
"""
