cdef extern from 'pari/pari.h':
    ctypedef long* GEN
    long bnrisconductor0(GEN A, GEN B, GEN C)
## would be nice to have bnrinit
#cdef extern from 'pari/pari.h':
#    ctypedef long* GEN
#    long bnrinit0(GEN bignf,GEN ideal,long flag)

from sage.libs.pari.gen cimport gen

#def pari_bnrinit(gen bnf, gen ideal):
#    return bnrinit0(bnf.g, ideal.g, 1)

def pari_bnrisconductor(gen bnf, gen ideal):
    return bnrisconductor0(bnf.g, ideal.g, NULL)
