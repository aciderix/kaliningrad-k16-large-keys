import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
import glob
from srcalign import *
W2=30   # smaller windows for short texts
def fold(t):
    t=t.lower().replace('ß','ss'); t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode(); return ''.join(c for c in t if c in A)
def wins(r,Wn): K=len(r)//Wn; return np.stack([np.bincount(r[k*Wn:(k+1)*Wn],minlength=len(KEEP)) for k in range(K)]).astype(np.float32) if K else None
def short_scan(src_r,bot_r,Wn=W2,minw=6):
    """slide source windows (fixed grid on source) against bottle reduced stream at every offset; per-window mean distance"""
    Sw=wins(src_r,Wn)
    if Sw is None or len(Sw)<minw: return None
    K=len(Sw); M=len(bot_r)
    if M < K*Wn: Sw=Sw[:M//Wn]; K=len(Sw)
    oh=np.zeros((M+1,len(KEEP)),np.float32); oh[np.arange(1,M+1),bot_r]=1; cum=np.cumsum(oh,0)
    best=(1e9,0)
    for g in range(0,M-K*Wn+1):
        B=np.stack([cum[g+Wn*(k+1)]-cum[g+Wn*k] for k in range(K)])
        d=(((B-Sw)**2)/(B+Sw+1)).sum()/K
        if d<best[0]: best=(d,g)
    return best,K
L=lines_v1(); bot_r=reduce(enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])))
if __name__=='__main__':
    rng=np.random.default_rng(3)
    if sys.argv[1]=='ctrl':
        # plant: a 400-letter German text, nulls 10%, chunk-20 scramble, embedded inside random German-like filler of the bottle's letters
        ho=german_corpus()['heldout']; src=ho[30000:30400]
        t=[]
        for c in src:
            t.append(c)
            if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
        t=enc(''.join(t)); 
        for i in range(0,len(t),20): t[i:i+20]=rng.permutation(t[i:i+20])
        filler=rng.permutation(enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])))
        stream=np.concatenate([filler[:300],t,filler[300:979-len(t)]])
        b=reduce(stream)
        (d,g),K=short_scan(reduce(enc(src)),b); print('planted short source: dist %.2f at %d (K=%d windows)'%(d,g,K))
        # distribution for unrelated short texts of same length
        ds=[]
        for k in range(60):
            st=int(rng.integers(0,len(ho)-500)); (d2,_),_=short_scan(reduce(enc(ho[st:st+400])),b); ds.append(d2)
        print('unrelated 400-letter texts: min %.2f median %.2f'%(min(ds),np.median(ds)))
    else:
        rows=[]
        for f in sys.argv[2:]:
            t=fold(open(f,encoding='utf-8',errors='ignore').read())
            r=short_scan(reduce(enc(t)),bot_r)
            if r: (d,g),K=r; rows.append((d,K,g,f))
        rows.sort()
        for d,K,g,f in rows[:15]: print(f'{d:6.2f} K={K:3d} at {g:4d} {os.path.basename(f)}')
        print('scanned',len(rows))
