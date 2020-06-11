from bitarray import bitarray # type: ignore
from typing import List
import pickle

#utility methods to deal with conversion to/from binary
def chunk(lst, chunk_size: int):
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i + chunk_size]

def lst_to_int(lst: List[bool]) -> int:
    #little endian
    total = 0
    for i in reversed(lst):
        total = (total << 1) ^ i
    return total

def int_to_bitarr(n: int, size: int) -> bitarray:
    #little endian
    arr = bitarray(size, endian='little')
    for i in range(size):
        arr[i] = n & 1
        n >>= 1
    return arr
        
def int_lst_to_bitarr(lst: List[int], chr_size: int) -> bitarray:
    msg_bits = bitarray(endian='little')
    for i in lst:
        msg_bits.extend(int_to_bitarr(i, chr_size))
    
    return msg_bits

def str_to_bitarr(msg: str, chr_size: int) -> bitarray:
    bitarr = bitarray(endian='little')
    bitarr.frombytes(bytes(msg,'ascii'))
    return bitarr

def str_to_int_lst(msg: str, chr_size: int) -> List[int]:
    bitarr = bitarray(endian='little')
    bitarr.frombytes(bytes(msg,'ascii'))
    return [lst_to_int(i) for i in chunk(bitarr, chr_size)]

def int_lst_to_str(lst: List[int], chr_size: int, msg_bit_len: int) -> str:
    last = lst[-1]

    msg_bits = bitarray(endian='little')
    for i in range(len(lst) - 1):
        msg_bits.extend(int_to_bitarr(lst[i], chr_size))
    
    #only some bits of the last character matter
    msg_bits.extend(int_to_bitarr(last, msg_bit_len - msg_bits.length()))
    return msg_bits.tobytes().decode('ascii')

def serialize(obj: object, filename: str) -> None:
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=-1)

def deserialize(filename: str) -> object:
    with open(filename, 'rb') as f:
        return pickle.load(f)

#utility for calculating probabilities of decoding success for lossy tdf
"""
def prob_bit(t: int):
    #probability any bit recovered
    return 1 - 0.75 ** t

def prob_char(c: int, t: int):
    bit = prob_bit(t)
    #probability all bits recovered
    return (1 - bit) ** c

def prob_success(p: float, m: int, thres: float):
    #probability that the sum(m draws of Bernoulli(p)) > thres
    from scipy.special import comb
    
    one_p = 1 - p

    prob = 0
    for i in range(thres):
        prob += comb(m,i)*(p**i)*(one_p**(m-i))
    return 1 - prob
""" 
