import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
import numpy as np
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain'); N=len(s); bc=Counter(s)
A='abcdefghijklmnopqrstuvwxyz'
texts=german_corpus()
if os.environ.get('K18_CLEAN'):
    keep=('g2229','g35312','g50285','g22367','g2407','g5323','g6498','g2403','g12108','g7205','heldout')
    texts={k:v for k,v in texts.items() if any(x in k for x in keep)}
allde=''.join(texts.values()); ct=Counter(allde); tot=len(allde)
p=np.array([(ct[a]+.5)/(tot+13) for a in A]); lp=np.log(p)
fi,wi,ni=A.index('f'),A.index('w'),A.index('n')
def G(c):
    c=np.asarray(c,float); n=c.sum(); m=c>0
    return 2*(c[m]*np.log(c[m]/(n*p[m]))).sum()
def best_removal(c, letters=(fi,wi,ni)):
    c=np.array(c,float); best=(G(c),(0,0,0))
    # coordinate grid search
    rf=range(0,int(c[fi])+1); rw=range(0,int(c[wi])+1); rn=range(0,int(c[ni])+1,2)
    for a in rf:
        for b in rw:
            for d in rn:
                cc=c.copy(); cc[fi]-=a; cc[wi]-=b; cc[ni]-=d
                g=G(cc)
                if g<best[0]: best=(g,(a,b,d))
    return best
cb=[bc[a] for a in A]
gb,rem=best_removal(cb)
print('bottle: G before %.1f ; best removal f,w,n = %s ; G after %.1f'%(G(cb),rem,gb))
# null: German windows, same optimisation (subsample for speed)
W=[[Counter(t[i:i+N])[a] for a in A] for t in texts.values() for i in range(0,len(t)-N,N)]
random.seed(2); W=random.sample(W,min(300,len(W)))
gs=[]
for w in W:
    gs.append(best_removal(w)[0])
gs=np.array(gs)
print('German windows after same optimisation: median %.1f, 95%% %.1f, max %.1f ; >= bottle: %d/%d'%(np.median(gs),np.quantile(gs,.95),gs.max(),(gs>=gb).sum(),len(gs)))
