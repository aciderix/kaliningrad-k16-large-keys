from periodic import *
rng=np.random.default_rng(77)
VOW=np.zeros(26,bool)
for c in 'aeiou': VOW[ix[c]]=True
def varwin(y,W):
    v=VOW[y].astype(float); c=np.convolve(v,np.ones(W),'valid'); return c.var()
def z(y,W,nn=2000):
    o=varwin(y,W); nb=np.array([varwin(rng.permutation(y),W) for _ in range(nn)]); return (o-nb.mean())/nb.std(), (nb<=o).mean()
L=lines_v1(); x=np.concatenate([enc(''.join(tokens(l,'plain'))) for l in L[:-1]])
for W in [10,20,40]:
    zz,p=z(x,W); print(f'bottle W={W}: z={zz:+.2f} p_low={p:.4f}')
ho=german_corpus()['heldout']
def ctrl(kind):
    st=rng.integers(0,len(ho)-1100); y=enc(ho[st:st+979]).copy()
    if kind.startswith('chunk'):
        Wc=int(kind.split()[1])
        for k in range(0,len(y),Wc): y[k:k+Wc]=rng.permutation(y[k:k+Wc])
    elif kind.startswith('period'):
        p=int(kind.split()[1]); perm=rng.permutation(p)
        for k in range(0,len(y)-p+1,p): y[k:k+p]=y[k:k+p][perm]
    elif kind=='columnar13': y=np.concatenate([y[i::13] for i in rng.permutation(13)])
    elif kind=='shuffle': y=rng.permutation(y)
    return y
for kind in ['in order','chunk 20','chunk 40','period 36','columnar13','shuffle']:
    res=[]
    for W in [10,20,40]:
        res.append(np.mean([z(ctrl(kind),W,300)[0] for _ in range(6)]))
    print(f'{kind:10s} mean z W=10,20,40: '+' '.join(f'{r:+.2f}' for r in res))
