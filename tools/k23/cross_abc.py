import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'habsig2.py')).read().split("o=stat(x,wid)")[0])
def cross(y,w,a=5,b=40):
    num=den=0
    for d in range(a,b+1):
        m=w[:-d]!=w[d:]; v=Ps[y[:-d],y[d:]]; num+=v[m].sum(); den+=m.sum()
    return num/den
o=cross(x,wid)
nul=np.array([cross(y,resegment(y)) for y in (rng.permutation(x) for _ in range(2000))])
print(f'1) signal entre mots, d=5-40 : z={(o-nul.mean())/nul.std():+.2f}, p={(nul>=o).mean():.4f} (2000 témoins)')
# 2) ABC on cross-word profile
B=[(5,10),(11,20),(21,40),(41,80)]
def prof(y,w):
    E=0
    return np.array([cross(y,w,a,b) for a,b in B])
texts=german_corpus(); pool=enc(''.join(v for k,v in texts.items() if any(t in k for t in ('g35312','g5323','g2407','g2229','heldout'))))
NW=np.array([ix['f'],ix['w'],ix['n']])
def sim(s,q):
    st=int(rng.integers(0,len(pool)-1400)); seg=pool[st:st+1400]; out=[]
    for c in seg:
        out.append(c)
        if rng.random()<q: out.append(NW[rng.integers(3)])
    y=np.array(out[:n])
    if s=='global': y=rng.permutation(y)
    else: y=y[np.argsort(np.arange(n)+rng.uniform(0,s,n))]
    return y
pb=prof(x,wid)
# centre profiles on their own shuffle expectation (cheap: 20 shuffles each) to remove composition effects
def centred(y,w):
    base=np.mean([prof(z,resegment(z)) for z in (rng.permutation(y) for _ in range(8))],0)
    return prof(y,w)-base
cb=centred(x,wid)
S=[];TH=[]
for i in range(900):
    s=int(rng.integers(1,151)); q=float(rng.uniform(0,.2)); y=sim(s,q); S.append(centred(y,resegment(y))); TH.append(s)
G=[centred(y,resegment(y)) for y in (sim('global',float(rng.uniform(0,.2))) for _ in range(200))]
S=np.array(S); TH=np.array(TH); G=np.array(G); sd=S.std(0)
d=np.sqrt((((S-cb)/sd)**2).sum(1)); thr=np.quantile(d,0.05); dg=np.sqrt((((G-cb)/sd)**2).sum(1))
for lo,hi in [(1,10),(11,30),(31,60),(61,100),(101,150)]:
    m=(TH>=lo)&(TH<=hi); print(f'   échelle {lo}-{hi}: part dans la zone retenue {np.mean(d[m]<=thr):.3f}')
print(f'   mélange global : {np.mean(dg<=thr):.3f}')
acc=TH[d<=thr]; print('   échelle retenue : médiane %.0f, 90%% [%.0f, %.0f]'%(np.median(acc),np.quantile(acc,.05),np.quantile(acc,.95)))
