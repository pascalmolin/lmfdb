# -*- coding: utf-8 -*-
# HeckeCharacters.py

from sage.all import ZZ, PowerSeriesRing, valuation
from sage.groups.abelian_gps.abelian_group import AbelianGroup_class
from sage.groups.abelian_gps.abelian_group_element import AbelianGroupElement
from sage.groups.abelian_gps.dual_abelian_group import DualAbelianGroup_class, DualAbelianGroupElement
from sage.groups.abelian_gps.dual_abelian_group import DualAbelianGroup_class, DualAbelianGroupElement
from pari_bnr import pari_bnrinit, pari_bnrisprincipal, pari_bnrconductorofchar

class RayClassGroup(AbelianGroup_class):
    """
    sage: k = NumberField(x^4-x^3+7,'a')
    sage: mod = k.ideal(25)
    sage: G = RayClassGroup(k,mod)
    sage: G.invariants()
    (200, 5, 5)
    """
    def __init__(self, number_field, mod_ideal = 1, mod_archimedean = None):
        if mod_archimedean == None:
            mod_archimedean = [0] * len(number_field.real_places())
        mod_ideal = number_field.ideal( mod_ideal )

        bnf = number_field.pari_bnf()
        # Use PARI to compute ray class group
        bnr = pari_bnrinit(bnf,pari([mod_ideal,mod_archimedean]),flag=1)
        # using pari index from 1
        # bnr[1] = bnf
        # bnr[2] = bid
        # bnr[3] = El ???
        # bnr[4] = gens
        # bnr[5] = clgp,    clgp[2]=cyc, clgp[3] = gens
        # bnr[6] = mat RU
        invariants = bnr[4][1]         # bnr.clgp.cyc
        invariants = tuple([ ZZ(x) for x in invariants ])
        names = tuple([ "I%i"%i for i in range(len(invariants)) ])
        generators = bnr[4][2]         # bnr.gen = bnr.clgp[3]
        generators = [ number_field.ideal(x) for x in generators ]

        AbelianGroup_class.__init__(self, invariants, names)
        self.__number_field = number_field
        self.__bnr = bnr
        #self.__pari_mod = bnr[1][0]
        self.__mod_ideal = mod_ideal
        self.__mod_arch = mod_archimedean
        self.__generators = generators

    #def __call__(self, *args, **kwargs):
    #    return group.Group.__call__(self, *args, **kwargs)

    def log(self,I):
        # Use PARI to compute class of given ideal
        g = pari_bnrisprincipal(self.__bnr,pari(I), flag = 0)
        g = [ ZZ(x) for x in g ]
        return g

    def number_field(self):
        return self.__number_field

    def bnr(self):
        return self.__bnr

    def modulus(self):
        return self.__mod_ideal

    def _element_constructor_(self, *args, **kwargs):
        try:
            return AbelianGroupElement(args[0], self)
        except:
            I = self.__number_field.ideal(*args, **kwargs)
            ### FIXME: should be faster
            if not I.is_coprime(self.__mod_ideal):
                return None
            return AbelianGroupElement(self.log(I), self)

    @cached_method
    def dual_group(self, base_ring=None):
        return HeckeCharGroup(self, base_ring)

    def __str__(self):
      return "Ray class group of modulus %s over %s" \
           %(self.modulus(),self.__number_field)
        
    def __repr__(self):
      return self.__str__()

    def gen_ideals(self):
        return self.__generators

    def exp(self,x):
        gens = self.gen_ideals()
        return prod( g**e for g,e in zip(gens,x) )

    def lift(self, x):
        return self.exp(x.exponents())

    def iter_exponents(self):
        for e in xmrange(self.invariants(), tuple):
            yield e

    def iter_ideals(self):
        for e in self.iter_exponents():
            yield self.exp(e)

    def character(self, exponents):
        return HeckeChar(self.dual_group(), exponents)


class HeckeCharGroup(DualAbelianGroup_class):
    def __init__(self, ray_class_group, base_ring):
        names = tuple([ "chi%i"%i for i in range(ray_class_group.ngens()) ])
        if base_ring is None:
            from sage.rings.number_field.number_field import CyclotomicField
            from sage.rings.arith import LCM
            base_ring = CyclotomicField(LCM(ray_class_group.gens_orders()))
        DualAbelianGroup_class.__init__(self, ray_class_group, names, base_ring)
        """ ray_class_group accessible as self.group() """

    def __call__(self, x):
        if isinstance(x, HeckeChar) and x.parent() is self:
            return x
        return HeckeChar(self, x)

    def __repr__(self):
        return "Group of Hecke characters on %s"%self.group()

    #def list(self):
    #    return [ HeckeChar(self, c.list()) for c in DualAbelianGroup_class.list(self) ]

    def primitive_characters(self):
        return [chi for chi in self.list() if chi.is_primitive() ]

class HeckeChar(DualAbelianGroupElement):

    def __init__(self, hecke_char_group, x):
        ray_class_group = hecke_char_group.group()
        if not isinstance(x, (list,tuple)) or len(x) != ray_class_group.ngens():
            x = ray_class_group(x).list()
        DualAbelianGroupElement.__init__(self, x, hecke_char_group)
        self.__repr = None
        self.__element_vector = x
        self.base_ring = CC

    #def __repr__(self):
    #    #return "Hecke character of index %s over %s" \
    #    #    %(self.list(),self.parent().group())
    #    return str(self.list())

    def number_field(self):
        return self.parent().group().number_field()

    def modulus(self):
        return self.parent().group().modulus()

    @cached_method
    def conductor(self):
        """
        sage: k = NumberField(x^4-x^3+7,'a')
        sage: mod = k.ideal(25)
        sage: chi = RayClassGroup(k,mod).character((20,1,0))
        sage: chi.conductor()
        Fractional ideal (-5*a^3 + 5*a + 20)
        """
        bnr = self.parent().group().bnr()
        chi = pari(self.exponents())
        pari_cond = pari_bnrconductorofchar(bnr,pari(chi))
        finite, arch = pari_cond
        return self.number_field().ideal(finite)

    def is_primitive(self):
        return self.conductor() == self.modulus()

    def logvalue(self, x):
        """
        sage: k = NumberField(x^4-x^3+7,'a')
        sage: mod = k.ideal(5)
        sage: chi = RayClassGroup(k,mod).dual_group().primitive_characters()[3]
        sage: chi.logvalue(5)
        """
        E = self.parent().group()(x)
        if E == None:
            return None
        E = E.exponents()
        F = self.exponents()
        D = self.parent().gens_orders()
        r = sum( e*f/d for e,f,d in zip( E, F, D) )
        if isinstance(r, (int,Integer)): return 0
        n,d = r.numerator(), r.denominator()
        return n%d/d

    def logvalues_on_gens(self):
        F = self.exponents()
        D = self.parent().gens_orders()
        return tuple( f/d for f,d in zip( F, D) )
        
    def __call__(self, x):
        try:
            logx = self.parent().group()(x)
        except:
            return 0
        return DualAbelianGroupElement.__call__(self,logx)

    def next_character(self, only_primitive=False):
        D = self.parent().gens_orders()
        F = list(self.exponents())
        i = len(D)-1
        while True:
            F[i] += 1
            if F[i] == D[i]:
                F[i] = 0
                i -= 1
                if i < 0: return None
            else:
                c = HeckeChar(self.parent(), F)
                if not only_primitive or c.is_primitive():
                    return c
               
    def prev_character(self, only_primitive=False):
        D = self.parent().gens_orders()
        F = list(self.exponents())
        i = len(D)-1
        while True:
            F[i] -= 1
            if F[i] < 0:
                F[i] = D[i] - 1
                i -= 1
                if i < 0: return None
            else:
                c = HeckeChar(self.parent(), F)
                if not only_primitive or c.is_primitive():
                    return c

    def galois_orbit(self):
        order = self.multiplicative_order()
        return [ self.__pow__(k) for k in xrange(order) if gcd(k,order) == 1 ]

    def dirichlet_series(self,n,prec=100):
        """ compute n coefficients of Dirichlet series

        sage: k = NumberField(x^4-x^3+7,'a')
        sage: mod = k.ideal(5)
        sage: chi = RayClassGroup(k,mod).dual_group().primitive_characters()[3]
        sage: sum(chi.dirichlet_series(300))
        98.304903507092841699573819276 + 97.335900978401476755022186609*I
        """
        k = self.number_field()
        a = [ 0 for i in xrange(n+1) ]
        a[1] = 1
        order = self.multiplicative_order()
        root = exp(2*I*pi.n(prec)/order)
        X = gen(PowerSeriesRing(root.parent(),'X'))
        for p in primes(n):
            """ compute Euler factor at p """
            maxpow = floor(log(n,p));
            Fp = 1+O(X**(maxpow+1))
            for P in k.primes_above(p):
                e,f = P.ramification_index(), P.residue_class_degree()
                chip = self.logvalue(P)
                if chip:
                    Fp *= (1-root**chip*X**f)**e
            """ expand the series """
            ap = 1/Fp
            if ap == 1:
                next
            """ sieve on values """
            for l in xrange(1,n//p+1):
                v = valuation(l,p)
                m = l // p**v
                a[l*p] = a[m] * ap[v+1]
        return a
        
    
"""
load('HeckeCharacters.py')
chi = RayClassGroup(k,13).dual_group()(3)
chi.dirichlet_series(20)


k.<a> = NumberField(x^4+7*x^2+13)
G = RayClassGroup(k,7)
H = G.dual_group()
H(3)
H([3,1])
"""
