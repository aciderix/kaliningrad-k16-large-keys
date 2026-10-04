from periodic import *
rng=np.random.default_rng(31)
Ps=P+P.T
BANDS=[(1,2),(3,5),(6,10),(11,20),(21,40),(41,80)]
def prof(y): return np.array([np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)]) for a,b in BANDS])
def zprof(y,nn=400):
    o=prof(y); nb=np.array([prof(rng.permutation(y)) for _ in range(nn)]); return (o-nb.mean(0))/nb.std(0)
L=lines_v1(); x=np.concatenate([enc(''.join(tokens(l,'plain'))) for l in L[:-1]])
print('bands      ',' '.join(f'{a}-{b}'.rjust(6) for a,b in BANDS))
print('bottle     ',' '.join(f'{v:+6.2f}' for v in zprof(x,1000)))
ho=german_corpus()['heldout']
words=re.findall(r'[a-zäöüß]+',open(CORP+'/g22367.txt',encoding='utf-8').read().lower()[3000:])
def german_words_stream(nlet):
    st=rng.integers(0,len(words)-400); out=[]
    i=st
    while sum(len(w) for w in out)<nlet:
        out.append(clean_de(words[i])); i+=1
    return out
def ctrl(kind):
    if kind=='word anagram':
        ws=german_words_stream(979); y=np.concatenate([rng.permutation(enc(w)) for w in ws if w])[:979]
        return y
    st=rng.integers(0,len(ho)-1100); y=enc(ho[st:st+979]).copy()
    if kind.startswith('chunk'):
        W=int(kind.split()[1])
        for k in range(0,len(y),W): y[k:k+W]=rng.permutation(y[k:k+W])
    elif kind.startswith('period'):
        p=int(kind.split()[1]); perm=rng.permutation(p)
        for k in range(0,len(y)-p+1,p): y[k:k+p]=y[k:k+p][perm]
    elif kind.startswith('jitter'):
        # each letter displaced by a random amount up to J (sort by i+U(0,J))
        J=int(kind.split()[1]); keys=np.arange(len(y))+rng.uniform(0,J,len(y)); y=y[np.argsort(keys)]
    return y
for kind in ['word anagram','chunk 10','chunk 20','chunk 40','chunk 80','period 16','period 36','jitter 10','jitter 30','jitter 60']:
    zs=np.array([zprof(ctrl(kind),200) for _ in range(5)])
    print(f'{kind:11s}',' '.join(f'{v:+6.2f}' for v in zs.mean(0)), '  (sd across 5: '+' '.join(f'{v:.1f}' for v in zs.std(0))+')')
