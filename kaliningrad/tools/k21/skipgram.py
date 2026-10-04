import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(91)
texts=german_corpus(); g=enc(''.join(texts.values())[:3000000])
def skipP(k):
    B=np.full((26,26),0.5); np.add.at(B,(g[:-k],g[k:]),1); u=np.bincount(g,minlength=26)+0.5
    return np.log(B/B.sum(1,keepdims=True))-np.log(u/u.sum())[None,:]
SP={k:skipP(k) for k in (1,2,3,4)}
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1]))
nul=[rng.permutation(x) for _ in range(1500)]
print('rows: plaintext skip k used for scoring ; cols: cipher distance d ; cells: z (symmetric score) vs 1500 shuffles')
for k in (1,2,3,4):
    Ps=SP[k]+SP[k].T; row=[]
    for d in (1,2,3,4,5,6):
        o=Ps[x[:-d],x[d:]].mean(); nb=np.array([Ps[y[:-d],y[d:]].mean() for y in nul]); row.append((o-nb.mean())/nb.std())
    print(f'plain skip {k}: '+' '.join(f'd{d}:{z:+.2f}' for d,z in zip((1,2,3,4,5,6),row)))
