from periodic import *
import time
L=lines_v1(); s=[]
for line in L[:-1]:
    for w in line.split(): s+=tokens(w,'plain')
x=enc(''.join(s))
def colpairs(x,p):
    K=26; st=list(range(0,len(x)-p+1,p)); nb=len(st)
    G=np.stack([x[a:a+p] for a in st])  # nb x p
    C=np.zeros((p,p,K,K))
    for i in range(p):
        for j in range(p):
            np.add.at(C[i,j],(G[:,i],G[:,j]),1)
    Cw=np.zeros((p,p,K,K))
    for i in range(p):
        for j in range(p):
            np.add.at(Cw[i,j],(G[:-1,i],G[1:,j]),1)
    return C,Cw
def MI(T):
    n=T.sum(); a=T.sum(1); b=T.sum(0); nz=T>0
    return (T[nz]/n*np.log(T[nz]*n/np.outer(a,b)[nz])).sum()
def table(perm,C,Cw):
    pr=np.array(perm); return C[pr[:-1],pr[1:]].sum(0)+Cw[pr[-1],pr[0]]
def anneal_mi(C,Cw,p,rng,iters=None,restarts=5):
    iters=iters or 3000+300*p; best=None
    for r in range(restarts):
        perm=list(rng.permutation(p)); cur=MI(table(perm,C,Cw))
        for it in range(iters):
            T=0.02*(1-it/iters)+1e-4
            i,j=sorted(rng.choice(p,2,replace=False)); m=rng.integers(3); q=perm[:]
            if m==0: q[i],q[j]=q[j],q[i]
            elif m==1: q[i:j+1]=q[i:j+1][::-1]
            else:
                seg=q[i:j+1]; del q[i:j+1]; k=rng.integers(len(q)+1); q[k:k]=seg
            sc=MI(table(q,C,Cw))
            if sc>=cur or rng.random()<math.exp((sc-cur)/T): perm,cur=q,sc
        if best is None or cur>best[0]: best=(cur,perm)
    return best
if __name__=='__main__':
    rng=np.random.default_rng(3)
    mode=sys.argv[1]
    ho=german_corpus()['heldout']
    if mode=='ctrl':
        for p in [5,8,12,16,20,25]:
            ok=0; out=[]
            for t in range(3):
                st=rng.integers(0,len(ho)-1000); y=enc(ho[st:st+979])
                sub=rng.permutation(26); y=sub[y]   # random substitution
                perm=rng.permutation(p); c=y.copy()
                for k in range(0,len(y)-p+1,p): c[k:k+p]=y[k:k+p][perm]
                C,Cw=colpairs(c,p); sc,found=anneal_mi(C,Cw,p,rng)
                true=list(np.argsort(perm)); ts=MI(table(true,C,Cw))
                ok+= found==true; out.append((round(sc,3),round(ts,3)))
            print(f'ctrl p={p} {ok}/3 {out}',flush=True)
    else:
        for p in range(2,26):
            C,Cw=colpairs(x,p); sc,perm=anneal_mi(C,Cw,p,rng)
            nul=[]
            for k in range(6):
                y=rng.permutation(x); C2,Cw2=colpairs(y,p); nul.append(anneal_mi(C2,Cw2,p,rng)[0])
            m=np.mean(nul); sd=np.std(nul)+1e-9
            print(f'p={p:2d} MI real {sc:.3f} null {m:.3f}±{sd:.3f} max {max(nul):.3f} z {(sc-m)/sd:+.1f}',flush=True)
