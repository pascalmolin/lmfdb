from HeckeCharacters import *
from pari_bnr import *

class GrossenCharacterLattice:

    def __init__(self,chi):
        """
        chi is a finite order Hecke character
        """
       
        self.k = chi.number_field()
        self
        self.bnf = self.k.pari_bnf()
        self.modulus = self.chi.modulus()
        """
        Now we have to select a basis of infinity type
        (a,b)  = (a_s), s : K->\C
                 (b_s), s : K->\C
        determining
        chi_i(x) = prod_{s\R} sgn(s(x))^a_s \prod_{s\C} (s(x)/|s(x)|)^a_s
                 * prod_{s\R} s(x)^ib_s \prod_{s\C} s(x)^ib_s
        such that
        chi_a,b(x) = 1 for any unit x = 1 mod m
        """

    def extend_torsion_units(self):
        """
        the infinity type on torsion units
        z = 1 mod m must be 1
        """
        self.tu = z = self.primitive_root_of_unity()
        self.order = self.tu.multiplicative_order()
        # compute the order mod m
        bnf = self.bnf
        bid = self.bnr.bid
        logz = ideallog(bid,z)
        pass

# latticesmallsols(M,y,d,lrange=1,startat=1) = {
#  my(s,s0,K,nk,L);
#  L = [];
#  s = matsolvemod(Mat(M),[d]~,[y]~,1);
#  /* s contains one solution and the kernel */
#  s0=s[1];K=s[2]; nk = matsize(K)[2]; L = [];
#  forvec(v=vector(nk,i,if(i<startat,[0,0],[-lrange,lrange])),
#    L = concat(L, [ (s0+K*v~)~ ] );
#    );
#  L;
#}       
#    
#hc_ext_tu(G,chi,lrange=1) = {
#  my(k,bid); k=G[1];bid=G[2];
#  order = k.tu[1];tu =k.tu[2];
#  logval = dceval(G,chi,tu)/bid.cyc[1] ; \\ order*logval is is an integer
#  if(order == 2, \\ then tu = -1 on each embedding
#    m = vector(k.r1+k.r2,j,1);
#    latticesmallsols(Mat(m),-order*logval,order,lrange,k.r1+1);
#    ,
#    \\ more units, so no real embedding
#    zC =  embeval(k,tu);
#    m = vector(k.r2,j,round(imag(log(zC[j]))*order/(2*Pi)));
#    latticesmallsols(Mat(m),-order*logval,order,lrange);
#    );
#}
