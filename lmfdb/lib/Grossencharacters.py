from sage.all import *
from HeckeCharacters import *

class GrossenCharacterLattice:

    def __init__(self,chi):
       
        self.k = chi.number_field()
        self.tu = self.primitive_root_of_unity()
        self.order = self.tu.multiplicative_order()
        """
        we have to first correct chi so that
        on each torsion unit z = 1 mod m
        chi(z) =
        """
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
