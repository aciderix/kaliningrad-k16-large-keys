from periodic import *
L=lines_v1(); s=[]
for line in L[:-1]:
    for w in line.split(): s+=tokens(w,'plain')
x=enc(''.join(s)); rng=np.random.default_rng(4)
Ps=P+P.T
def band(y,a=1,b=10): return np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)])
def winshuf(y,W,rng):
    y=y.copy(); off=rng.integers(W)
    for k in range(-off,len(y),W):
        a=max(k,0); b=min(k+W,len(y)); y[a:b]=rng.permutation(y[a:b])
    return y
def same_pairs(y,D=10): return sum((y[:-d]==y[d:]).sum() for d in range(1,D+1))
obs=band(x); osp=same_pairs(x)
for W in [0,80,40,20]:
    nb=[]; ns=[]
    for _ in range(1000):
        y=rng.permutation(x) if W==0 else winshuf(x,W,rng)
        nb.append(band(y)); ns.append(same_pairs(y))
    nb=np.array(nb); ns=np.array(ns)
    print(f"null {'global' if W==0 else 'window '+str(W):10s}: band1-10 z={(obs-nb.mean())/nb.std():+.2f} p={(nb>=obs).mean():.3f} | same-letter pairs d<=10: obs {osp} null {ns.mean():.1f} z={(osp-ns.mean())/ns.std():+.2f}")
