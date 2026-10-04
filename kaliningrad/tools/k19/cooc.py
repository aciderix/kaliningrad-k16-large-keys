from periodic import *
rng=np.random.default_rng(21)
L=lines_v1(); x=np.concatenate([enc(''.join(tokens(l,'plain'))) for l in L[:-1]])
D=10
def cooc(y,D=D):
    C=np.zeros((26,26))
    for d in range(1,D+1):
        np.add.at(C,(y[:-d],y[d:]),1)
    return C+C.T
def enrich(y,nn=300):
    o=cooc(y); nul=np.array([cooc(rng.permutation(y)) for _ in range(nn)])
    return o, nul.mean(0), nul.std(0)+1e-9
o,m,sd=enrich(x)
z=(o-m)/sd
# German reference local co-occurrence enrichment (in-order German, which equals local-scramble expectation for |d|<=D roughly)
ho=german_corpus()['heldout']
yg=enc(ho[10000:30000]); og=cooc(yg)
fg=np.bincount(yg,minlength=26)/len(yg); eg=np.outer(fg,fg)*og.sum()
lr=np.log((og+1)/(eg+1))   # German local enrichment log-ratio
present=[i for i in range(26) if (x==i).sum()>=6]
pairs=[(i,j) for a,i in enumerate(present) for j in present[a:]]
zz=np.array([z[i,j] for i,j in pairs]); ll=np.array([lr[i,j] for i,j in pairs])
r=np.corrcoef(zz,ll)[0,1]
# permutation null for correlation: recompute with shuffled bottle
rn=[]
for _ in range(200):
    y=rng.permutation(x); oy=cooc(y); zy=(oy-m)/sd
    rn.append(np.corrcoef(np.array([zy[i,j] for i,j in pairs]),ll)[0,1])
rn=np.array(rn)
print(f'correlation bottle local-enrichment vs German local co-occurrence: r={r:+.3f}; null {rn.mean():+.3f}±{rn.std():.3f}; z={(r-rn.mean())/rn.std():+.2f}; p={(rn>=r).mean():.3f}')
for pr in ['ch','sc','sh','ck','ei','ie','en','er','nd','ng','st','un','au','ge','ht','tz','ff','ss','nn','ll','ee','fw','iu','ae']:
    i,j=ix[pr[0]],ix[pr[1]]
    print(f'  {pr}: bottle obs {o[i,j]:.0f} exp {m[i,j]:.1f} z={z[i,j]:+.2f} | German local log-ratio {lr[i,j]:+.2f}')
