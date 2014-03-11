
include 'sage/ext/stdsage.pxi'
include 'sage/ext/interrupt.pxi'

from sage.structure.sage_object cimport SageObject

cdef extern from 'pari/pari.h':
    ctypedef long* GEN
    long bnrisconductor0(GEN A, GEN B, GEN C)
    GEN bnrinit0(GEN bnf, GEN ideal, long flag)
    GEN bnrisprincipal(GEN bnr, GEN ideal, long flag)
    GEN bnrconductorofchar(GEN bnr, GEN chi)

import sage.libs.pari.gen
from sage.libs.pari.gen cimport gen, PariInstance

cdef PariInstance instance = <PariInstance>sage.libs.pari.gen.pari

def pari_bnrisconductor(gen bnf, gen ideal):
    """
    sage: bnf = pari('bnfinit(y^7+y^2+131,1)')
    sage: pari_bnrisconductor(bnf,pari('[11,[1]]'))
    1
    """
    return bnrisconductor0(bnf.g, ideal.g, NULL)

def pari_bnrinit(gen bnf, gen ideal, flag=1):
    """
    sage: bnf = pari('bnfinit(y^16-232*y^14+17564*y^12-592696*y^10+10090294*y^8-87937112*y^6+356253116*y^4-482477960*y^2+143400625,1)')
    sage: bnr = pari_bnrinit(bnf, pari('60'))
    sage: bnr[4][1] # bnr.clgp.cyc
    [48, 8, 8, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2]
    """
    sig_on()
    return instance.new_gen(bnrinit0(bnf.g, ideal.g, flag))

def pari_bnrisprincipal(gen bnr, gen ideal, flag=0):
    """
    sage: bnr = pari('bnrinit(bnfinit(y^16-232*y^14+17564*y^12-592696*y^10+10090294*y^8-87937112*y^6+356253116*y^4-482477960*y^2+143400625,1),13)')
    sage: pari_bnrisprincipal(bnr, pari('3'))
    [16, 0, 0, 0]~
    """
    sig_on()
    return instance.new_gen(bnrisprincipal(bnr.g, ideal.g, flag))

def pari_bnrconductorofchar(gen bnr, gen chi):
    """
    sage: bnf = pari('bnfinit(y^7+y^2+131,1)')
    sage: bnr = pari_bnrinit(bnf,pari('[13,[1]]'))
    sage: bnr[4][1]
    [12]
    sage: pari_bnrconductorofchar(bnr, pari('[3]'))
    [[13, 0, 0, 0, 0, 0, 1; 0, 13, 0, 0, 0, 0, 9; 0, 0, 13, 0, 0, 0, 3; 0, 0, 0, 13, 0, 0, 1; 0, 0, 0, 0, 13, 0, 9; 0, 0, 0, 0, 0, 13, 3; 0, 0, 0, 0, 0, 0, 1], [1]]
    """
    sig_on()
    return instance.new_gen(bnrconductorofchar(bnr.g, chi.g))
