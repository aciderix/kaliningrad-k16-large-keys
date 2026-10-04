import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(19)
Pa=P-P.T   # forward minus backward
def asym(y,a=1,b=8): return np.mean([Pa[y[:-d],y[d:]].mean() for d in range(a,b+1)])
def fwd(y,a=1,b=8): return np.mean([P[y[:-d],y[d:]].mean() for d in range(a,b+1)])
def z(y,f,nn=1000):
    o=f(y); nb=np.array([f(rng.permutation(y)) for _ in range(nn)]); return (o-nb.mean())/nb.std()
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1]))
print('bottle: asymmetry z (d1-8) = %+.2f ; forward-score z (d1-8) = %+.2f'%(z(x,asym),z(x,fwd)))
print('bottle per distance asym z:',' '.join(f'{d}:{z(x,lambda y:asym(y,d,d),400):+.1f}' for d in range(1,9)))
ho=german_corpus()['heldout']
def interleave(q,st):
    msg=list(ho[st:st+2000]); out=[]
    while len(out)<979:
        if rng.random()<q: out.append(msg.pop(0))
        else: out.append('fwnerl'[rng.integers(6)])
    return enc(''.join(out))
def chunk(k,st):
    y=enc(ho[st:st+979]).copy()
    for i in range(0,979,k): y[i:i+k]=rng.permutation(y[i:i+k])
    return y
for name,gen in [('fillers q=0.6',lambda s:interleave(0.6,s)),('fillers q=0.4',lambda s:interleave(0.4,s)),('fillers q=0.25',lambda s:interleave(0.25,s)),('chunk-20 anagram',lambda s:chunk(20,s))]:
    res=[(z(gen(st),asym,300),z(gen(st),fwd,300)) for st in (10000,30000,50000)]
    print(f'{name:18s} asym z: '+' '.join(f'{a:+.1f}' for a,_ in res)+' | fwd z: '+' '.join(f'{b:+.1f}' for _,b in res))
