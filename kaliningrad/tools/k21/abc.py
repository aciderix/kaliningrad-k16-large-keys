import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(2026)
Ps=P+P.T
BANDS=[(1,2),(3,5),(6,10),(11,20),(21,40),(41,80)]
def stats(y):
    n=len(y); c=np.bincount(y,minlength=26).astype(float)
    E=(c@Ps@c-(c*np.diag(Ps)).sum())/(n*(n-1))
    out=[]
    for a,b in BANDS:
        out.append(np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)])-E)
    return np.array(out)
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])); n=len(x)
sb=stats(x)
texts=german_corpus(); pool=enc(''.join(v for k,v in texts.items() if any(t in k for t in ('g22367','g35312','g2407','g5323','g2229','heldout'))))
NULLW=np.array([ix['f'],ix['w'],ix['n']])
def sim(kind,s,q):
    st=int(rng.integers(0,len(pool)-1400)); seg=pool[st:st+1400]
    m=rng.random(1400)<q; out=[]
    for i,cc in enumerate(seg):
        out.append(cc)
        if m[i]: out.append(NULLW[rng.integers(3)])
    y=np.array(out[:n])
    if kind=='jitter' and s>0: y=y[np.argsort(np.arange(n)+rng.uniform(0,s,n))]
    elif kind=='chunk' and s>1:
        off=int(rng.integers(s))
        for a in range(-off,n,s): y[max(0,a):a+s]=rng.permutation(y[max(0,a):a+s])
    elif kind=='global': y=rng.permutation(y)
    return y
NS=int(sys.argv[1]) if len(sys.argv)>1 else 3000
res={}
for kind in ('jitter','chunk'):
    S=[];TH=[]
    for i in range(NS):
        s=int(rng.integers(1,121)); q=float(rng.uniform(0,0.25))
        S.append(stats(sim(kind,s,q))); TH.append((s,q))
    S=np.array(S); TH=np.array(TH)
    sd=S.std(0); dist=np.sqrt((((S-sb)/sd)**2).sum(1))
    k=int(0.03*NS); idx=np.argsort(dist)[:k]
    acc=TH[idx]
    res[kind]=(dist[idx].mean(),acc)
    print(f'{kind}: mean accepted distance {dist[idx].mean():.2f} | scale s: median {np.median(acc[:,0]):.0f}, 90% [{np.quantile(acc[:,0],.05):.0f}, {np.quantile(acc[:,0],.95):.0f}] | nulls q: median {np.median(acc[:,1]):.2f}, 90% [{np.quantile(acc[:,1],.05):.2f}, {np.quantile(acc[:,1],.95):.2f}]',flush=True)
# reference: global shuffle and no scramble distances
for kind in ('global',):
    S2=np.array([stats(sim(kind,0,float(rng.uniform(0,.25)))) for _ in range(300)])
    sd=S2.std(0)
print('bottle stats:',np.round(sb,4))
