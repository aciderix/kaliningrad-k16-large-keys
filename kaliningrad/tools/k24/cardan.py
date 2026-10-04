import os, sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(3)
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])); n=len(x)
def best_path(blocks,m):
    """max over i1<...<im of sum_k S[ik,ik+1], S summed over blocks; returns mean score per edge"""
    p=blocks.shape[1]; S=np.zeros((p,p))
    for b in blocks: S+=P[b[:,None],b[None,:]]
    S/=len(blocks)
    tri=np.triu(np.ones((p,p),bool),1); S=np.where(tri,S,-1e9)
    V=np.zeros(p)                       # best path of length 1 ending at j
    for k in range(1,m):
        V=(V[:,None]+S).max(0)
    return V.max()/(m-1)
def blocks_of(y,p,off): 
    K=(len(y)-off)//p; return np.stack([y[off+k*p:off+(k+1)*p] for k in range(K)])
def scan(y,p,frac):
    m=max(4,int(p*frac)); return max(best_path(blocks_of(y,p,off),m) for off in range(0,p,max(1,p//8)))
mode=sys.argv[1]
ho=german_corpus()['heldout']
if mode=='ctrl':
    for p in (49,100,169):
        for frac in (0.3,0.5):
            m=int(p*frac); holes=np.sort(rng.choice(p,m,replace=False)); msg=enc(ho[5000:5000+(n//p)*m+10]); y=rng.permutation(x).copy()
            k=0
            for b in range(n//p):
                y[b*p+holes]=msg[k:k+m]; k+=m
            r=scan(y,p,frac); nul=[scan(rng.permutation(x),p,frac) for _ in range(5)]
            print(f'contrôle p={p} trous={frac}: plantée {r:+.3f} | lettres mélangées max {max(nul):+.3f}',flush=True)
else:
    for p in (25,36,49,64,81,100,121,144,169):
        for frac in (0.25,0.4,0.6):
            r=scan(x,p,frac); nul=[scan(rng.permutation(x),p,frac) for _ in range(6)]
            print(f'p={p:3d} trous={frac}: bouteille {r:+.3f} | mélanges {np.mean(nul):+.3f} (max {max(nul):+.3f})',flush=True)
