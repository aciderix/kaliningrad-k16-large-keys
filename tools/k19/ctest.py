from periodic import *
rng=np.random.default_rng(17)
L=lines_v1(); lines=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
x=np.concatenate(lines); sizes=[len(l) for l in lines]
C,H,K=ix['c'],ix['h'],ix['k']
def stat_lines(ls):
    tot=0; ok=0
    for y in ls:
        nc=(y==C).sum()
        if nc==0: continue
        partners=(y==H).sum()+(y==K).sum()
        # each c needs its own h/k: count min(nc, partners)
        tot+=nc; ok+=min(nc,partners)
    return ok,tot
def stat_window(y,W=6):
    pos=np.where(y==C)[0]; ok=0
    for p in pos:
        seg=np.concatenate([y[max(0,p-W):p],y[p+1:p+1+W]])
        ok+= ((seg==H)|(seg==K)).any()
    return ok,len(pos)
o=stat_lines(lines); ow=[stat_window(x,W) for W in (3,6,10)]
nl=[]; nw={3:[],6:[],10:[]}
for _ in range(5000):
    y=rng.permutation(x); ls=[]; i=0
    for z in sizes: ls.append(y[i:i+z]); i+=z
    nl.append(stat_lines(ls)[0])
    for W in (3,6,10): nw[W].append(stat_window(y,W)[0])
nl=np.array(nl)
print(f'c with an h/k partner in the same line: {o[0]}/{o[1]} ; null mean {nl.mean():.1f} ; p_high={(nl>=o[0]).mean():.4f}')
for (W,(ok,t)) in zip((3,6,10),ow):
    a=np.array(nw[W]); print(f'c with h/k within ±{W}: {ok}/{t} ; null mean {a.mean():.1f} ; p_high={(a>=ok).mean():.4f}')
# German reference: what fraction in German chunk-anagrams of 40?
ho=german_corpus()['heldout']; y=enc(ho[:200000]); chunks=[y[i:i+40] for i in range(0,len(y)-40,40)]
print('German 40-letter chunks: c with h/k partner in chunk: %d/%d'%stat_lines(chunks))
for l,orig in zip(lines,L[:-1]):
    if (l==C).any(): print('  line has c:', ''.join(A[i] for i in l), '| h:',(l==H).sum(),'k:',(l==K).sum())
