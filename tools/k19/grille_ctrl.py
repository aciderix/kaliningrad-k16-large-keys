from grille import *
rng=np.random.default_rng(5)
ho=german_corpus()['heldout']
def with_nulls(t,rate=0.10):
    out=[]
    for c in t:
        out.append(c)
        if rng.random()<rate: out.append('fwn'[rng.integers(3)])
    return ''.join(out)
for n in [4,5,6]:
    p=n*n
    for variant in ['plain','nulls','nulls+reversed']:
        t0=time.time(); ok=0; info=[]
        for trial in range(3):
            st=rng.integers(0,len(ho)-2000)
            t=ho[st:st+979] if variant=='plain' else with_nulls(ho[st:st+900])[:979]
            if 'reversed' in variant: t=t[::-1]
            y=enc(t)
            ccw=bool(rng.integers(2)); seqs,ch=all_sequences(n,ccw); j=rng.integers(len(seqs)); seq=seqs[j]
            off=int(rng.integers(p)); c=y.copy()
            for k in range(off,len(y)-p+1,p):
                blk=np.empty(p,dtype=y.dtype); blk[seq]=y[k:k+p]; c[k:k+p]=blk   # plaintext letter i written in cell seq[i]
            res=search(c,n)
            b=res[0]; good = (b[1]==ccw and not b[2] and b[3]=='off%d'%off and np.array_equal(b[6],seq))
            # equivalent keys (e.g. rotated start) count if decryption identical
            if not good:
                dec=lambda s,o: np.concatenate([c[k:k+p][s] for k in range(o,len(c)-p+1,p)])
                o2=int(b[3][3:]) if b[3].startswith('off') else -1
                if o2==off and not b[2]:
                    d1=dec(b[6],off); d1=d1 if not b[4] else d1
                    good=np.array_equal(d1,dec(seq,off))
            ok+=good; info.append((round(b[0],3),b[3],'rev' if b[4] else 'fwd'))
        print(f'n={n} {variant:15s} recovered {ok}/3 {info} {time.time()-t0:.0f}s',flush=True)
