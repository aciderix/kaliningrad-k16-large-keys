import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'habsig2.py')).read().split("o=stat(x,wid)")[0])
texts=german_corpus(); pool=enc(''.join(v for k,v in texts.items() if 'g35312' in k or 'g5323' in k))
for kind,s in [('jitter',50),('jitter',25),('chunk',50)]:
    res=[]
    for r in range(4):
        st=int(rng.integers(0,len(pool)-1200)); y=pool[st:st+n].copy()
        if kind=='jitter': y=y[np.argsort(np.arange(n)+rng.uniform(0,s,n))]
        else:
            for a in range(0,n,s): y[a:a+s]=rng.permutation(y[a:a+s])
        w=resegment(y); o=stat(y,w)
        nul=[]
        for _ in range(400):
            z=rng.permutation(y); nul.append(stat(z,resegment(z)))
        nul=np.array(nul); res.append([(o[j]-nul[:,j].mean())/nul[:,j].std() for j in (0,1)])
    res=np.array(res)
    print(f'contrôle {kind} {s}: dans un mot z = '+' '.join(f'{v:+.1f}' for v in res[:,0])+' | entre mots z = '+' '.join(f'{v:+.1f}' for v in res[:,1]))
