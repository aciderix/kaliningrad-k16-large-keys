import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *; from dewin import *
import numpy as np
rng=np.random.default_rng(21)
texts=german_corpus(); pool=''.join(v for k,v in texts.items() if any(t in k for t in ('g22367','g35312','g2407','g5323','heldout')))
for kind,k in [('chunk',20),('chunk',40),('chunk',80),('jitter',60),('global',0)]:
    for r in range(3):
        st=int(rng.integers(0,len(pool)-2000)); t=[]
        for c in pool[st:st+1300]:
            t.append(c)
            if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
        t=np.array(t[:979])
        if kind=='chunk':
            off=int(rng.integers(k))
            for a in range(-off,979,k): t[max(0,a):a+k]=rng.permutation(t[max(0,a):a+k])
        elif kind=='jitter': t=t[np.argsort(np.arange(979)+rng.uniform(0,k,979))]
        else: t=rng.permutation(t)
        open(f'wc_{kind}{k}_{r}.txt','w').write(''.join(t)+'\n')
