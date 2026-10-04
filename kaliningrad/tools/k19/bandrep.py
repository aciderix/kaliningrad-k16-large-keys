from periodic import *
rng=np.random.default_rng(12)
Ps=P+P.T
def band(y,a=1,b=10): return np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)])
def zband(y,nn=1000):
    o=band(y); nb=np.array([band(rng.permutation(y)) for _ in range(nn)])
    return (o-nb.mean())/nb.std(), o-nb.mean()
L=lines_v1()
v1=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
cs=open(ROOT+'data/transcription_corsair_2015.txt',encoding='utf-8').read().split('\n')
cs=[l for l in cs if l and not l.startswith('#')][:24]
cor=[enc(''.join(c for c in tokens(l,'plain') if c in ix)) for l in cs]
print('v1 full        z=%+.2f eff=%+.4f'%zband(np.concatenate(v1)))
print('corsair full   z=%+.2f eff=%+.4f'%zband(np.concatenate(cor)))
print('v1 odd lines   z=%+.2f eff=%+.4f'%zband(np.concatenate(v1[0::2])))
print('v1 even lines  z=%+.2f eff=%+.4f'%zband(np.concatenate(v1[1::2])))
print('v1 page1       z=%+.2f eff=%+.4f'%zband(np.concatenate(v1[:20])))
print('v1 page2       z=%+.2f eff=%+.4f'%zband(np.concatenate(v1[20:])))
# within-line only pairs (no pair spanning a line break): compute band on each line separately pooled
def band_lines(ls,a=1,b=10):
    num=0; den=0
    for y in ls:
        for d in range(a,min(b,len(y)-1)+1):
            num+=Ps[y[:-d],y[d:]].sum(); den+=len(y)-d
    return num/den
o=band_lines(v1); x=np.concatenate(v1); sizes=[len(l) for l in v1]
nb=[]
for _ in range(1000):
    y=rng.permutation(x); ls=[]; i=0
    for z in sizes: ls.append(y[i:i+z]); i+=z
    nb.append(band_lines(ls))
nb=np.array(nb); print('v1 within-line pairs z=%+.2f'%((o-nb.mean())/nb.std()))
# controls: German transformed, each vs own shuffles
ho=german_corpus()['heldout']
def ctrl(kind):
    st=rng.integers(0,len(ho)-1100); y=enc(ho[st:st+979]).copy()
    if kind=='in order': pass
    elif kind=='period16':
        perm=rng.permutation(16)
        for k in range(0,len(y)-15,16): y[k:k+16]=y[k:k+16][perm]
    elif kind=='period36':
        perm=rng.permutation(36)
        for k in range(0,len(y)-35,36): y[k:k+36]=y[k:k+36][perm]
    elif kind=='columnar13':
        y=np.concatenate([y[i::13] for i in rng.permutation(13)])
    elif kind=='double 11x13':
        y=np.concatenate([y[i::11] for i in rng.permutation(11)]); y=np.concatenate([y[i::13] for i in rng.permutation(13)])
    elif kind=='grille 13x13 blocks':
        # random fixed permutation of 169 per block (proxy for grille)
        perm=rng.permutation(169)
        for k in range(0,len(y)-168,169): y[k:k+169]=y[k:k+169][perm]
    elif kind=='line anagram (~40)':
        for k in range(0,len(y),40): y[k:k+40]=rng.permutation(y[k:k+40])
    return zband(y,300)
for kind in ['in order','period16','period36','columnar13','double 11x13','grille 13x13 blocks','line anagram (~40)']:
    zs=[ctrl(kind) for _ in range(6)]
    print(f'ctrl {kind:20s} z: '+' '.join(f'{z:+.1f}' for z,_ in zs)+'   eff: '+' '.join(f'{e:+.3f}' for _,e in zs))
