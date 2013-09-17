
include 'sage/ext/stdsage.pxi'
include 'sage/ext/interrupt.pxi'

from sage.structure.sage_object cimport SageObject

cdef extern from 'pari/pari.h':
    ctypedef long* GEN
    long bnrisconductor0(GEN A, GEN B, GEN C)
    GEN bnrinit0(GEN bignf, GEN ideal, long flag)

import sage.libs.pari.gen
from sage.libs.pari.gen cimport gen, PariInstance

cdef PariInstance instance = <PariInstance>sage.libs.pari.gen.pari

def pari_bnrisconductor(gen bnf, gen ideal):
    return bnrisconductor0(bnf.g, ideal.g, NULL)

def pari_bnrinit(gen bignf, gen ideal, flag=1):
    """
    sage: bnf = pari('bnfinit(y^16-232*y^14+17564*y^12-592696*y^10+10090294*y^8-87937112*y^6+356253116*y^4-482477960*y^2+143400625)')
    sage: pari_bnrinit(bnf, pari('60'))
    """
    sig_on()
    return instance.new_gen(bnrinit0(bignf.g, ideal.g, flag))
