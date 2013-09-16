from sage.all import *

class NFIdeals(dict):

  def __init__(self, k, primelimit=100):
    self.k = k
    self.prime = {}
    self.tree = {}
    #self.labels = {}
    for p in primes(primelimit):
      self._add_prime(p)
    
  def _add_prime(self,p):
      fp = self.k.primes_above(p)
      Lp = {}
      #if len(fp) == 1:
      #   gp = Lp[1]
      #   self[p] = {gp.residue_class_degree():(str(p),gp)}
      for gp in fp:
        f = gp.residue_class_degree()
        if f not in Lp:
          Lp[f] = []
        Lp[f].append(gp)
      for f in Lp.keys():
        if len(Lp[f]) == 1:
          [gp] = Lp[f]
          label = '%i-%i'%(p,f)
          Lp[f] = [ (label, gp) ]
          self[gp] = label
          self.prime[label] = gp
        else:
          Lf = sorted(Lp[f]) # which sort ???? by embedding ???
          Lp[f] = [ ( '%i-%i%s'%(p,f,chr(i+97)) ,gp) for i,gp in enumerate(Lf) ]
          for label,gp in Lp[f]:
            self[gp] = label
            self.prime[label] = gp
      self.tree[p] = Lp

  def primelabels(self):
    R = []
    for Lp in self.tree.values():
      for Lpf in Lp.values():
        for gp in Lpf:
          R.append(gp[0])
    return R

  def label(self,ideal):
    f = self.k.ideal(ideal).factor()
    return '.'.join( [self._primelabel(p,e) for p,e in f ] )

  def _primelabel(self,p,e=1):
    if p not in self:
      self._add_prime(p.pari_prime()[0])
    if e == 1:
      return self[p]
    else:
      return '%s^%i'%(self[p],e)

  def reduce(self,powers):
    pass

  # todo: need to do a right generator
  #def ideals_of_norm(self, n):
  #  for p,e in factor(n):
  #    lf = self.tree[p].keys()
  #    for a in mrange([ e//f for f in lf]):
  #      if a*lf != e: next
  #      for ef in Partitions(

  #    for f,lf in self.tree[p]
  #    forvec(a=vector(#wp,k,[0,ep\wp[k]]),
  #      if(a*wp~==ep, Lp = concat(Lp, [ idealfactorback(k,fp,a)] ))

  def first_ideals(self,n):
    pass


  def fromlabel(self, label):
    ideal = 1 
    for plabel in label.split('.'):
      if '^' in plabel:
        plabel,e = plabel.split('^')
      else:
        e = 1
      p,fe = plabel.split('-')
      ideal *= self.prime[plabel]**e
    return ideal
