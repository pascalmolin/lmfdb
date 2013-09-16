cdef extern from 'pari/pari.h':
    ctypedef long* GEN
    long bnrisconductor0(GEN A, GEN B, GEN C)

from sage.libs.pari.gen cimport gen

def pari_bnrisconductor(gen bnf, gen ideal):
    return bnrisconductor0(bnf.g, ideal.g, NULL)

