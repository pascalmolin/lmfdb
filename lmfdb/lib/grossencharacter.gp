/*for tests*/
k = bnfinit(x^4+x^3+7);

/*
 compute a list of first prime decompositions
 over number field k
 and order primes:
  - first by inertia degree
  - then by complex embeddings
 return a list [prime, [ list of primes dividing ] ]
 */
smallprimeslistandname(k,pmax) = {
  my(n=poldegree(k.pol));
  my(L = vector(primepi(pmax)));
  my(l = 0);
  my(sep="-");
  forprime(p=2,pmax,
      my(fp = idealprimedec(k,p));
      my(Lp=[]);
      /* if p is inert or totally ramified, no need to label */
      if(#fp == 1,
        fp = fp[1];
        if(fp.f == n,
          /* inert */ 
          Lp = [ [Str(p),p ] ], /* or Str(p,sep,n) and fp ? */
          Lp = [ [Str(p,sep,1),fp] ]
          );
        ,
        /* first order and split by inertia degree */
        (fsort(a,b)=if(a.f!=b.f,b.f-a.f,
                       a.e!=b.e,b.e-a.e,
                       t2a=a[2]~*k.t2*a[2];
                       t2b=b[2]~*k.t2*b[2];
                       sign(t2b-t2a)
                       ));
        fp = vecsort(fp,fsort);
        \\Lp = [ [ fp[1].f, [ fp[1] ] ] ];
        my(f=0); my(j);
        for(i=1,#fp,
          print(i,fp[i]);
          \\if(fp[i].f == Lp[j][1],
          if(fp[i].f!=f, f = fp[i].f; j=1);
            \\Lp[j][2] = concat(Lp[j][2],[fp[i]]),
            Lp = concat(Lp, [ [ Str(p,sep,f,Strchr(96+j)), fp[i] ] ]); j++;
            \\Lp = concat(Lp, [ fp[i].f, [ fp[i] ] ] ); j++
            \\);
          );
        );
      L[l++] = [p,Lp];
      );
  L;
}
idealnames(k,pmax) = {
  my(L = smallprimeslistandname(k,pmax));
  concat( [ [ p[1] | p <- l[2] ] | l <- L ]);
}

idealsbynormprod(k,n) = {
  if(n==1, return([ [ idealhnf(k,1) ] ] ));
  fz = factor(n);
  r = matsize(fz)[1];
  L = vector(r);
  for(i=1,r,
      my(Lp = []);
      p=fz[i,1];ep=fz[i,2];
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
  my(k,bid); k=G[1];bid=G[2];
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


/* small solutions M*x=y mod dZ in Z^r */
latticesmallsols(M,y,d,lrange=1,startat=1) = {
  my(s,s0,K,nk,L);
  L = [];
  s = matsolvemod(Mat(M),[d]~,[y]~,1);
  /* s contains one solution and the kernel */
  s0=s[1];K=s[2]; nk = matsize(K)[2]; L = [];
  forvec(v=vector(nk,i,if(i<startat,[0,0],[-lrange,lrange])),
    L = concat(L, [ (s0+K*v~)~ ] );
    );
  L;
}


/* first find extension on torsion units */
/* returns a Z/dZ basis up to dZ, where d is the order of torsion */
hc_ext_tu(G,chi,lrange=1) = {
  my(k,bid); k=G[1];bid=G[2];
  order = k.tu[1];tu =k.tu[2];
  logval = dceval(G,chi,tu)/bid.cyc[1] ; \\ order*logval is is an integer
  if(order == 2, \\ then tu = -1 on each embedding
    m = vector(k.r1+k.r2,j,1);
    latticesmallsols(Mat(m),-order*logval,order,lrange,k.r1+1);
    ,
    \\ more units, so no real embedding
    zC =  embeval(k,tu);
    m = vector(k.r2,j,round(imag(log(zC[j]))*order/(2*Pi)));
    latticesmallsols(Mat(m),-order*logval,order,lrange);
    );
}


/* then on fundamental units */
hc_ext_fu(G,chi,tors,lrange=1) = {
  my(k,bid); k=G[1];bid=G[2];
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
  \\print(m);
  b = concat(b, 0);
  m = log(abs(Mat(m~)));
  /* put factors 2 for complex embeddings */
  \\for(j=k.r1+1,r+1,for(i=1,r+1,m[i,j]*=2));
  /* now solve mod the lattice Z^r */
  my(L=[]);
  forvec(v=vector(#b,i,[-lrange,lrange]),
    s = matsolve(m,Col(b+v));
    L = concat(L,[Vec(s)]);
    );
  L;
}

/* now a complete Hecke Grossencharacter is a tuple
 * [dirichlet char, inftytu, inftyfu]
 */
gclist(G,chi,turange=1,furange=1) = {
  my(L = []);
  tuinf = hc_ext_tu(G,chi,turange);
  for(t=1,#tuinf,
     tors = tuinf[t];
     L = concat(L,[ [chi,tors,inf] | inf <- hc_ext_fu(G,chi,tors,furange) ]);
     );
  L;
}


gceval(G,gc,x) = {
  my(k,bid); k=G[1];bid=G[2];
  my(chi,tuinf,fuinf);chi=gc[1];tuinf=gc[2];fuinf=gc[3];
  x = bnfisprincipal(k,x)[2]; 
  xC = embeval(k,x);
  vf = vector(#xC,i,if(i<=k.r1,if(xC[i]<0,1/2,0),arg(xC[i])/(2*Pi)));
  vi = log(abs(xC));
  t = dceval(G,chi,x) + tuinf*vf~ + fuinf*vi~;
  t%1;
}
       
gcconductoranalytic(G,gc) = {
  my(k,bid); k=G[1];bid=G[2];
  my(chi,tuinf,fuinf);chi=gc[1];tuinf=gc[2];fuinf=gc[3];
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

gclistbyanalyticconductor(G,chi,turange=0,furange=0) = {
  L = gclist(G,chi,turange,furange);
  Lc = [ [gc,gcconductoranalytic(G,gc)] | gc <- L ];
  vecsort(Lc,2);
  \\[ lc[1] | lc <- vecsort(Lc,2) ];
}

gcdirseries(G,gc,pmax=500) = {
  my(k,bid); k=G[1];bid=G[2];
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
