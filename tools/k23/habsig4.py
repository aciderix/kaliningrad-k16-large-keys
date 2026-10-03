import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'habsig2.py')).read().split("o=stat(x,wid)")[0])
BANDS=[(1,4),(5,10),(11,20),(21,40)]
def bands(y,w):
    r=[]
    for a,b in BANDS:
        for same in (True,False):
            num=den=0
            for d in range(a,b+1):
                m=(w[:-d]==w[d:]) if same else (w[:-d]!=w[d:]); v=Ps[y[:-d],y[d:]]; num+=v[m].sum(); den+=m.sum()
            r.append(num/den if den else np.nan)
    return np.array(r)
o=bands(x,wid); nul=[]
for _ in range(800):
    y=rng.permutation(x); nul.append(bands(y,resegment(y)))
nul=np.array(nul); z=(o-np.nanmean(nul,0))/np.nanstd(nul,0)
for i,(a,b) in enumerate(BANDS): print(f'd {a:2d}-{b:2d}: dans un mot z={z[2*i]:+.2f} | entre mots z={z[2*i+1]:+.2f}')
# c -> h/k within ±10, split same word / different word
C,H,K=ix['c'],ix['h'],ix['k']
def cstat(y,w):
    same=diff=0
    for p in np.where(y==C)[0]:
        for q in range(max(0,p-10),min(n,p+11)):
            if q!=p and y[q] in (H,K):
                if w[q]==w[p]: same+=1
                else: diff+=1
    return same,diff
cs=cstat(x,wid); cn=np.array([cstat(y,resegment(y)) for y in (rng.permutation(x) for _ in range(1500))])
print(f'paires c–h/k à ±10 : même mot {cs[0]} (témoin {cn[:,0].mean():.1f}, z={(cs[0]-cn[:,0].mean())/cn[:,0].std():+.2f}) ; mots différents {cs[1]} (témoin {cn[:,1].mean():.1f}, z={(cs[1]-cn[:,1].mean())/cn[:,1].std():+.2f})')
# position within word: score of adjacent pairs (d=1) inside words by position (start pair, middle, end pair)
def pos(y,w):
    res={'debut':[], 'milieu':[], 'fin':[]}
    for i in range(n-1):
        if w[i]!=w[i+1]: continue
        start=(i==0 or w[i-1]!=w[i]); end=(i+2>=n or w[i+2]!=w[i+1])
        res['debut' if start else ('fin' if end else 'milieu')].append(Ps[y[i],y[i+1]])
    return {k:np.mean(v) for k,v in res.items()}
op=pos(x,wid); pn=[pos(y,resegment(y)) for y in (rng.permutation(x) for _ in range(800))]
for k in op:
    a=np.array([p[k] for p in pn]); print(f'paires voisines en {k:6s} de mot : z={(op[k]-a.mean())/a.std():+.2f}')
