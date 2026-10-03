from periodic import *
rng=np.random.default_rng(23)
L=lines_v1(); x=np.concatenate([enc(''.join(tokens(l,'plain'))) for l in L[:-1]])
C,H,K=ix['c'],ix['h'],ix['k']
def nearest(y,cap=60):
    hk=np.where((y==H)|(y==K))[0]; out=[]
    for p in np.where(y==C)[0]:
        out.append(min(cap,np.abs(hk-p).min()))
    return np.array(out)
db=nearest(x); print('bottle c->nearest h/k distances:',sorted(db.tolist()))
ho=german_corpus()['heldout']; base=enc(ho[20000:220000])
def scramble(y,kind,W):
    y=y.copy()
    if kind=='chunk':
        off=rng.integers(W)
        for k in range(-off,len(y),W):
            a=max(0,k); y[a:k+W]=rng.permutation(y[a:k+W])
    elif kind=='jitter':
        y=y[np.argsort(np.arange(len(y))+rng.uniform(0,W,len(y)))]
    elif kind=='global': y=rng.permutation(y)
    return y
# likelihood of bottle distances under each model via simulated distance distribution (binned)
bins=[0,1,2,3,4,6,8,11,15,20,30,61]
def hist(d): return np.histogram(d,bins=bins)[0]
hb=hist(db)
print('bins',bins); print('bottle',hb)
for kind,W in [('chunk',10),('chunk',20),('chunk',30),('chunk',40),('chunk',60),('jitter',10),('jitter',20),('jitter',40),('global',0)]:
    sims=[]
    for r in range(20):
        seg=base[r*9000:(r+1)*9000]
        sims.append(nearest(scramble(seg,kind,W)))
    sd=np.concatenate(sims); pr=(hist(sd)+0.5)/(len(sd)+0.5*len(hb))
    ll=(hb*np.log(pr)).sum()
    print(f'{kind:6s} W={W:3d} loglik={ll:7.2f}  median dist={np.median(sd):5.1f}  frac<=10={np.mean(sd<=10):.2f}')
# bottle-specific null: global shuffle of bottle letters (accounts for bottle h/k density)
nb=[np.mean(nearest(rng.permutation(x))<=10) for _ in range(3000)]
print('bottle frac<=10 = %.2f ; bottle-shuffle null mean %.2f'%(np.mean(db<=10),np.mean(nb)))
