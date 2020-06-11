# Deterministic Encryption using Trapdoor Functions

Implementation of the DDH based Linear Trapdoor Function for deterministic encryption outlined in the following paper.

New Techniques for Efficient Trapdoor Functions and Applications
Sanjam Garg, Romain Gay, Mohammad Hajiabadi

https://eprint.iacr.org/2018/872.pdf


### Build

This project requires Python3.7

Install dependencies and setup the project using pipenv or pip:
    
    make build


### Example usage

Encoding and Decoding example:
    
    from ddh_tdf import KG

    x: bytes = b'\x00\x01\x02'
    #Initialize index and trapdoor keys with maximum encodable message length
    ik, tk = KG(length = len(x) * 8)

    #alternatively, deserialize existing keys from files
    #ik = deserialize(filename)
    #tk = deserialize(filename)
  
    u: DDH_TDF_CipherText = ik.encode(x)
    result: bytes = tk.decode(u)

### Benchmarking and Testing

Time the performance of important functions, optional LEN argument to change size of structures:

    make benchmark LEN=(size of msg in bytes)


Run the unit tests using the unittest package:

    make test


Remove build, test, benchmark files:

    make clean


Other options are listed:

    make help


### Dependency

The TDF construction depends on arithmetic over ed25519 points implemented by floodberry at:

    https://github.com/floodyberry/ed25519-donna

A cython interface was written for floodberry's package so it could be used in this python TDF construction and is built during (`make build`).
