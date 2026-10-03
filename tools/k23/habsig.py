import os, sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(5)
Ps=P+P.T
L=lines_v1(); letters=[]; wid=[]; k=0
for line in L[:-1]:
    for w in line.split():
        t=tokens(w,'plain')
        if t: letters+=t; wid+=[k]*len(t); k+=1
x=enc(''.join(letters)); wid=np.array(wid); n=len(x)
def stat(y,D):
    out={}
    for name,mask_fn in [('meme mot',lambda d: wid[:-d]==wid[d:]),('mots differents',lambda d: wid[:-d]!=wid[d:])]:
        num=0; den=0
        for d in range(1,D+1):
            m=mask_fn(d); v=Ps[y[:-d],y[d:]]; num+=v[m].sum(); den+=m.sum()
        out[name]=num/den
    return out
for D in (2,4,8):
    o=stat(x,D); nul=[stat(rng.permutation(x),D) for _ in range(1500)]
    for key in o:
        a=np.array([u[key] for u in nul]); print(f'd<={D} {key:16s} z={(o[key]-a.mean())/a.std():+.2f}')
