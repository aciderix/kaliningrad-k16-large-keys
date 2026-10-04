from periodic import *
import time
L=lines_v1()
# stream and section bounds
s=[]; bounds=[]; a=0
for line in L[:-1]:
    for w in line.split():
        s+=tokens(w,'plain')
        if '_' in w: bounds.append((a,len(s))); a=len(s)
x=enc(''.join(s))
rng=np.random.default_rng(7)
NNULL=int(sys.argv[1]) if len(sys.argv)>1 else 8
print('p mode real | null mean max | z | best decryption head')
for p in range(2,65):
    for mode in ['global','sections']:
        sc,perm,st=run(x,p,mode,bounds,rng)
        nul=[]
        for k in range(NNULL):
            y=rng.permutation(x); nul.append(run(y,p,mode,bounds,rng)[0])
        m=np.mean(nul); sd=np.std(nul)+1e-9
        # decrypt head
        g=[]; 
        for st0 in st[:4]:
            grp=x[st0:st0+p]; g+= [A[grp[j]] for j in perm]
        print(f"{p:2d} {mode:8s} {sc:6.3f} | {m:6.3f} {max(nul):6.3f} | {(sc-m)/sd:+5.1f} | {''.join(g)[:48]}",flush=True)
