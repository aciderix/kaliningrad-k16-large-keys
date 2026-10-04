import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *; from dewin import *
import numpy as np
rng=np.random.default_rng(55)
texts=german_corpus(); pool=''.join(v for k,v in texts.items() if any(t in k for t in ('g22367','g35312','g2407','g5323','heldout')))
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
arr=np.array([ix[c] for c in pool[:2000000]])
def markov(order,n):
    if order==1:
        T=np.full((26,26),0.01); np.add.at(T,(arr[:-1],arr[1:]),1); T/=T.sum(1,keepdims=True)
        s=[int(rng.integers(26))]
        for _ in range(n-1): s.append(int(rng.choice(26,p=T[s[-1]])))
    else:
        T=np.full((26,26,26),0.01); np.add.at(T,(arr[:-2],arr[1:-1],arr[2:]),1); T/=T.sum(2,keepdims=True)
        s=[int(rng.integers(26)),int(rng.integers(26))]
        for _ in range(n-2): s.append(int(rng.choice(26,p=T[s[-2],s[-1]])))
    return ''.join(A[i] for i in s)
for order in (1,2):
    for r in range(3):
        t=[]
        for c in markov(order,1300):
            t.append(c)
            if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
        t=np.array(t[:979]); off=int(rng.integers(20))
        for a in range(-off,979,20): t[max(0,a):a+20]=rng.permutation(t[max(0,a):a+20])
        open(f'ps_markov{order}_{r}.txt','w').write(''.join(t)+'\n')
