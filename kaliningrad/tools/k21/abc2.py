import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'abc.py')).read().split("NS=int")[0])
rng2=np.random.default_rng(7)
# reference set to standardise: jitter sims (prior)
S=[];TH=[]
for i in range(2000):
    s=int(rng.integers(1,121)); q=float(rng.uniform(0,0.25)); S.append(stats(sim('jitter',s,q))); TH.append(s)
S=np.array(S); sd=S.std(0); d=np.sqrt((((S-sb)/sd)**2).sum(1)); thr=np.quantile(d,0.03)
G=np.array([stats(sim('global',0,float(rng.uniform(0,.25)))) for _ in range(600)])
dg=np.sqrt((((G-sb)/sd)**2).sum(1))
N0=np.array([stats(sim('none',0,float(rng.uniform(0,.25)))) for _ in range(300)])
d0=np.sqrt((((N0-sb)/sd)**2).sum(1))
TH=np.array(TH)
for lo,hi in [(1,10),(11,25),(26,50),(51,80),(81,120)]:
    m=(TH>=lo)&(TH<=hi); print(f'jitter s in [{lo},{hi}]: fraction within threshold {np.mean(d[m]<=thr):.3f}')
print(f'global shuffle: fraction within threshold {np.mean(dg<=thr):.3f} ; no scramble: {np.mean(d0<=thr):.3f} (threshold {thr:.2f})')
