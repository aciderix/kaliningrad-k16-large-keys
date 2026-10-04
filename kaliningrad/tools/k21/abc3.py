import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'abc.py')).read().split("NS=int")[0])
SEC=[(0,166),(166,335),(335,497),(497,666),(666,835),(835,979)]
def sim2(kind,s,q):
    y=sim('none',0,q)
    if kind=='sections':
        for a,b in SEC: y[a:b]=rng.permutation(y[a:b])
    elif kind=='chunk': 
        off=int(rng.integers(s))
        for a in range(-off,n,s): y[max(0,a):a+s]=rng.permutation(y[max(0,a):a+s])
    elif kind=='jitter': y=y[np.argsort(np.arange(n)+rng.uniform(0,s,n))]
    return y
# reference sims across a wide prior to standardise and set threshold
REF=[];TH=[]
for i in range(3000):
    kind=['chunk','jitter'][i%2]; s=int(rng.integers(1,201)); q=float(rng.uniform(0,.25))
    REF.append(stats(sim2(kind,s,q))); TH.append((i%2,s))
REF=np.array(REF); TH=np.array(TH); sd=REF.std(0); d=np.sqrt((((REF-sb)/sd)**2).sum(1)); thr=np.quantile(d,0.03)
for lo,hi in [(1,25),(26,50),(51,80),(81,120),(121,160),(161,200)]:
    m=(TH[:,1]>=lo)&(TH[:,1]<=hi); print(f's in [{lo},{hi}]: within threshold {np.mean(d[m]<=thr):.3f}  (n={m.sum()})')
Ssec=np.array([stats(sim2('sections',0,float(rng.uniform(0,.25)))) for _ in range(600)])
ds=np.sqrt((((Ssec-sb)/sd)**2).sum(1))
print(f'shuffle within the 6 real sections: within threshold {np.mean(ds<=thr):.3f} (n=600) ; threshold {thr:.2f}')
acc=TH[d<=thr]; print('accepted s: median %.0f, 90%% [%.0f, %.0f]'%(np.median(acc[:,1]),np.quantile(acc[:,1],.05),np.quantile(acc[:,1],.95)))
