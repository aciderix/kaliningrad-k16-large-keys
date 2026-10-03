import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(71)
D=10
def cooc(y):
    C=np.zeros((26,26))
    for d in range(1,D+1): np.add.at(C,(y[:-d],y[d:]),1)
    return C+C.T
# German local co-occurrence log-ratio from in-order German (equivalent to local scramble expectation)
texts=german_corpus(); g=enc(''.join(v for k,v in texts.items() if 'heldout' in k or 'g35312' in k)[:300000])
og=cooc(g); fg=np.bincount(g,minlength=26)/len(g); eg=np.outer(fg,fg)*og.sum(); LR=np.log((og+1)/(eg+1))
def letter_corr(y,nn=300):
    o=cooc(y); nul=np.array([cooc(rng.permutation(y)) for _ in range(nn)]); m=nul.mean(0); sd=nul.std(0)+1e-9
    z=(o-m)/sd; zn=(nul-m)/sd
    cnt=np.bincount(y,minlength=26); res={}
    for X in range(26):
        if cnt[X]<6: continue
        part=[j for j in range(26) if cnt[j]>=6 and j!=X]
        r=np.corrcoef(z[X,part],LR[X,part])[0,1]
        rn=np.array([np.corrcoef(zn[k,X,part],LR[X,part])[0,1] for k in range(nn)])
        res[A[X]]=(r,(r-rn.mean())/rn.std(),cnt[X])
    return res
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1]))
res=letter_corr(x)
print('bottle: per-letter correlation of local neighbourhood with German (z vs shuffles)')
for a,(r,z,c) in sorted(res.items(),key=lambda t:-t[1][1]): print(f'  {a} n={c:3d} r={r:+.2f} z={z:+.2f}')
# control: German + nulls f/w (random positions) + chunk-20 scramble: are nulls detected as low-z?
ho=german_corpus()['heldout']; t=[]
for c in ho[20000:21100]:
    t.append(c)
    if rng.random()<0.06: t.append('f')
    if rng.random()<0.04: t.append('w')
t=enc(''.join(t[:979])).copy()
for i in range(0,979,20): t[i:i+20]=rng.permutation(t[i:i+20])
rc=letter_corr(t)
print('control (German + 6% null f + 4% null w, chunk-20):')
print('  '+' '.join(f'{a}:{z:+.1f}' for a,(r,z,c) in sorted(rc.items(),key=lambda t:-t[1][1])))
