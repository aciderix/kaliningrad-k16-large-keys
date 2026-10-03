import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from shortalign import *
rng=np.random.default_rng(17)
ho=german_corpus()
pool=''.join(ho.values())
print('K   planted(dist)   unrelated: min over 2000, 1st percentile')
for Lsrc in (260,350,500,700):
    st=int(rng.integers(0,len(pool)-5000)); src=pool[st:st+Lsrc]
    t=[]
    for c in src:
        t.append(c)
        if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
    t=enc(''.join(t))
    for i in range(0,len(t),40): t[i:i+40]=rng.permutation(t[i:i+40])
    filler=rng.permutation(enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])))
    stream=np.concatenate([filler[:200],t,filler[200:979-len(t)]])[:979]
    (dp,_),K=short_scan(reduce(enc(src)),reduce(stream))
    ds=[]
    for k in range(2000):
        s2=int(rng.integers(0,len(pool)-Lsrc-10)); r=short_scan(reduce(enc(pool[s2:s2+Lsrc])),bot_r)
        if r: ds.append(r[0][0])
    ds=np.array(ds)
    print(f'{K:2d}  {dp:6.2f}   min {ds.min():.2f}   1% {np.quantile(ds,0.01):.2f}   median {np.median(ds):.2f}',flush=True)
