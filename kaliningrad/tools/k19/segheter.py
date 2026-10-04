from periodic import *
L=lines_v1()
lines=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
x=np.concatenate(lines); n=len(x); rng=np.random.default_rng(8)
def chi2(segs):
    tot=np.bincount(np.concatenate(segs),minlength=26); N=tot.sum(); X=0
    for s in segs:
        c=np.bincount(s,minlength=26); e=len(s)*tot/N; m=e>0
        X+=((c[m]-e[m])**2/e[m]).sum()
    return X
def split(y,sizes):
    out=[]; i=0
    for z in sizes: out.append(y[i:i+z]); i+=z
    return out
ho=german_corpus()['heldout']; kant=german_corpus()
de=''.join(v for k,v in kant.items() if any(t in k for t in ('heldout','g22367','g35312','g2407')))
for name,sizes in [('lines (25)',[len(l) for l in lines]),('W=20',[20]*(n//20)),('W=40',[40]*(n//40)),('W=80',[80]*(n//80)),('W=160',[160]*(n//160))]:
    m=sum(sizes)
    obs=chi2(split(x[:m],sizes))
    nul=np.array([chi2(split(rng.permutation(x)[:m],sizes)) for _ in range(2000)])
    # German natural level: contiguous German windows of m letters split the same way (no shuffle)
    gz=[]
    for k in range(200):
        st=rng.integers(0,len(de)-m-1); y=enc(de[st:st+m])
        yn=np.array([chi2(split(rng.permutation(y),sizes)) for _ in range(30)])
        gz.append((chi2(split(y,sizes))-yn.mean())/yn.std())
    gz=np.array(gz)
    print(f"{name:10s} bottle chi2={obs:7.1f} null={nul.mean():7.1f}±{nul.std():5.1f} z={(obs-nul.mean())/nul.std():+.2f} p={(nul>=obs).mean():.4f} | German in order: z median {np.median(gz):+.2f} (5-95%: {np.quantile(gz,.05):+.2f}..{np.quantile(gz,.95):+.2f})")
