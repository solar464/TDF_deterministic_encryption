from floodberry.floodberry_ed25519 import GE25519 as GE
from utils import serialize

serialize(GE(1), "temp/1.p")
serialize([GE(1)], "temp/1_list.p")
serialize([GE(1), GE(2)], "temp/2.p")
serialize([GE(i) for i in range(10)], "temp/10.p")
serialize([GE(i) for i in range(100)], "temp/100.p")
