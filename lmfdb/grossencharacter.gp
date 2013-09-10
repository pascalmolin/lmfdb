
idealsbynormprod(k,n) = {
  if(n==1, return([ [ idealhnf(k,1) ] ] ));
  fz = factor(n);
  r = matsize(fz)[1];
  L = vector(r);
  for(i=1,r,
      my(Lp = []);
      [p,ep] = fz[i,];
      fp = [ pk | pk <- idealprimedec(k,p), pk.f <= ep ];
      if(fp==[],return([])); \\ no solution
      wp = [ pk.f | pk <- fp ];
      /* now loop over all sum a[i]*wp[i] = ep */
      forvec(a=vector(#wp,k,[0,ep\wp[k]]),
        if(a*wp~==ep, Lp = concat(Lp, [ idealfactorback(k,fp,a)] ))
        );
      if(Lp == [], return([]) );
      L[i] = Lp;
     );
  L;
}

prodtolist(k,Lp) = {
  if(Lp == [], return([]));
  np = #Lp;
  L = [];
  forvec(v=vector(np,i,[1,#Lp[i]]),
    i = 1; id = Lp[i][v[i]];
    for(i=2,#v,id = idealmul(k,id,Lp[i][v[i]]));
    L = concat(L,[id]);
    );
  L;
}

idealsbynorm(k,n) = prodtolist(k,idealsbynormprod(k,n));

checkideallist(k,n) = {
  L1 = apply(vecsort, ideallist(k,n,4) );
  L2 = vector(n,i,vecsort(idealsbynorm(k,i)));
  L1 == L2;
}

dcinit(k,mod) = [k,idealstar(k,mod,2)];
dcchar(G,chi) = cyc=G[2].cyc;vector(#cyc,i,chi[i]*cyc[1]/cyc[i])%cyc[1];
dceval(G,chi,x) = {
  my(k,bid); [k,bid] = G;
  chi * ideallog(k,x,bid)%bid.cyc[1];
  }
/* eval at embeddings */
embeval(k,z) = {
  my(a);
  if(type(z)=="t_COL",   z=nfbasistoalg(k,z));
  a = lift(z); my(d = poldegree(a));
  my(emb = k.roots);
  vector(#emb,j, sum(k=0,d,polcoeff(a,k)*emb[j]^k));
}
/* find grossencharacters having Dirichlet part chi */

/* first find extension on torsion units */
/* returns a Z/dZ basis up to dZ, where d is the order of torsion */
hc_ext_tu(G,chi,zrange=0) = {
  my(k,bid); [k,bid] = G;
  [order, tu] = k.tu;
  logval = dceval(G,chi,tu)/bid.cyc[1] ; \\ order*logval is is an integer
  if(order == 2, \\ then tu = -1 on each embedding
    m = vector(k.r1+k.r2,j,1);
    ,
    \\ more units, so no real embedding
    zC =  embeval(k,tu);
    m = vector(k.r2,j,round(imag(log(zC[j]))*order/(2*Pi)));
    );
    print([order, m, logval]);
    s = matsolvemod(Mat(m),[order]~,[-order*logval]~,1)[2];
    apply(mattranspose,Vec(s));
}


/* then on fundamental units */
hc_ext_fu(G,chi,tors,zrange=0) = {
  my(k,bid); [k,bid] = G;
  expo = bid.cyc[1];
  fu = k.fu;
  r = #fu;
  m = vector(r,i,embeval(k,fu[i]));
  b = vector(r,i,
    - dceval(G,chi,fu[i])
     - tors * round(imag(log(m[i]))/(2*Pi)*expo)~;
  );
  /* add one row for the diagonal embedding */
  m = concat(m, [vector(r+1,i,2)]);
  print(m);
  b = concat(b, 0);
  m = log(abs(Mat(m~)));
  /* put factors 2 for complex embeddings */
  \\for(j=k.r1+1,r+1,for(i=1,r+1,m[i,j]*=2));
  s = matsolve(m,Col(b));
  Vec(s);
}

/* now a complete Hecke Grossencharacter is a tuple
 * [dirichlet char, inftytu, inftyfu]
 */
gclist(G,chi) = {
  L = [];
  tuinf = hc_ext_tu(G,chi);
  for(t=1,#tuinf,
     tors = tuinf[t];
     L = concat(L,[ [chi,tors,hc_ext_fu(G,chi,tors)] ]);
     );
  L;
}

gceval(G,gc,x) = {
  my(k,bid); [k,bid] = G;
  my(chi,tuinf,fuinf);[chi,tuinf,fuinf]=gc;
  x = bnfisprincipal(k,x)[2]; 
  xC = embeval(k,x);
  vf = vector(#xC,i,if(i<=k.r1,if(xC[i]<0,1/2,0),arg(xC[i])/(2*Pi)));
  vi = log(abs(xC));
  t = dceval(G,chi,x) + tuinf*vf~ + fuinf*vi~;
  t%1;
}
       
gcconductoranalytic(G,gc) = {
  my(k,bid); [k,bid] = G;
  my(chi,tuinf,fuinf);[chi,tuinf,fuinf]=gc;
  s = 0;
  for(i=1,k.r1,
    s += polcoeff(lngamma((1/2-I*tuinf[i]+fuinf[i]+x+O(x^2))/2),1);
    );
  for(i=k.r1+1,k.r1+k.r2,
    s += polcoeff(lngamma(1/2-I*tuinf[i]/2+(fuinf[i]-1)/2+x+O(x^2)),1);
    );
  mod = bid[1];
  sqrt( abs(k.disc*idealnorm(k,mod))/Pi^poldegree(k.pol))*exp(2*real(s)); 
}

gcdirseries(G,gc,pmax=500) = {
  my(k,bid); [k,bid] = G;
  direuler(p=2,pmax,
    f = idealprimedec(k,p);
    prod(i=1,#f,
      (1-gceval(G,gc,f[i])*X^f[i].f)^f[i].e
     );
    );
}

  
do(P=x^4+x^3+7,mod=14,chi) = {
  k = bnfinit(P,1);
  G = dcinit(k,mod);
  if(chi,
  L = gclist(G,chi);
  L = [ [gc,gcconductoranalytic(G,gc)] | gc <- L ];
  L = vecsort(L,2);
  L;
  ,
  G[2].cyc;
  );
}
  
    

