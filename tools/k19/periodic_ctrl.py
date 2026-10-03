from periodic import *
import time
rng=np.random.default_rng(1)
ho=german_corpus()['heldout']
# insert ~10% nulls f/w/n variant
def with_nulls(t,rng,rate=0.10):
    out=[]
    for c in t:
        out.append(c)
        if rng.random()<rate: out.append('fwn'[rng.integers(3)])
    return ''.join(out)
for p in [4,7,12,16,25,36,49,64]:
    for variant in ['plain','nulls']:
        ok=0; tt=time.time(); res=[]
        for trial in range(3):
            st=rng.integers(0,len(ho)-2000)
            t=ho[st:st+979] if variant=='plain' else with_nulls(ho[st:st+900],rng)[:979]
            x=enc(t); perm=rng.permutation(p)
            # encrypt: within each complete group, cipher[k*p+j]=plain[k*p+perm[j]]
            c=x.copy()
            for k in range(0,len(x)-p+1,p): c[k:k+p]=x[k:k+p][perm]
            sc,found,stt=run(c,p,'global',None,rng)
            # true order: plaintext position perm[j] is at cipher j -> reading order = argsort(perm)
            true=list(np.argsort(perm))
            S,Sw,nb=mats(c,p,stt); tsc=score(np.array(true),S,Sw)/(nb*(p-1)+len(stt)-1)
            succ = found==true
            ok+=succ; res.append((round(sc,3),round(tsc,3)))
        print(f"p={p:2d} {variant:6s} success {ok}/3  (found,true) {res}  {time.time()-tt:.1f}s",flush=True)
