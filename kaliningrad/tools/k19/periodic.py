import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *; from dewin import *
import numpy as np
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
texts=german_corpus(); pool=''.join(texts.values())
# German bigram log-ratio matrix
B=np.full((26,26),0.5); u=np.full(26,0.5)
arr=np.frombuffer(pool.encode(),dtype=np.uint8)-97
np.add.at(B,(arr[:-1],arr[1:]),1); np.add.at(u,arr,1)
P=np.log(B/B.sum(1,keepdims=True))-np.log(u/u.sum())[None,:]
def enc(s): return np.array([ix[c] for c in s])
def mats(x,p,starts):
    """column adjacency scores over complete groups starting at given positions"""
    S=np.zeros((p,p)); Sw=np.zeros((p,p)); nb=0; nw=0
    for st in starts:
        g=x[st:st+p]
        S+=P[g[:,None],g[None,:]]; nb+=1
    for a,b in zip(starts,starts[1:]):
        if b==a+p:
            Sw+=P[x[a:a+p][:,None],x[b:b+p][None,:]]; nw+=1
    return S,Sw,nb
def score(perm,S,Sw):
    return S[perm[:-1],perm[1:]].sum()+Sw[perm[-1],perm[0]]
def anneal(S,Sw,p,rng,iters=None,restarts=6):
    iters=iters or 4000+400*p
    best=None
    for r in range(restarts):
        perm=list(rng.permutation(p)); cur=score(np.array(perm),S,Sw)
        T0=2.0; 
        for it in range(iters):
            T=T0*(1-it/iters)+1e-3
            i,j=sorted(rng.choice(p,2,replace=False))
            m=rng.integers(3)
            q=perm[:]
            if m==0: q[i],q[j]=q[j],q[i]
            elif m==1: q[i:j+1]=q[i:j+1][::-1]
            else:
                seg=q[i:j+1]; del q[i:j+1]; k=rng.integers(len(q)+1); q[k:k]=seg
            sc=score(np.array(q),S,Sw)
            if sc>=cur or rng.random()<math.exp((sc-cur)/T): perm,cur=q,sc
        if best is None or cur>best[0]: best=(cur,perm)
    return best
def starts_global(n,p): return list(range(0,n-p+1,p))
def starts_sections(bounds,p):
    st=[]
    for a,b in bounds: st+=list(range(a,b-p+1,p))
    return st
def run(x,p,mode,bounds,rng):
    st=starts_global(len(x),p) if mode=='global' else starts_sections(bounds,p)
    S,Sw,nb=mats(x,p,st)
    sc,perm=anneal(S,Sw,p,rng)
    nbig=nb*(p-1)+ (len(st)-1)
    return sc/nbig, perm, st
