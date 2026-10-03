from grille import *
L=lines_v1(); s=[]; bounds=[]; a=0
for line in L[:-1]:
    for w in line.split():
        s+=tokens(w,'plain')
        if '_' in w: bounds.append((a,len(s))); a=len(s)
x=enc(''.join(s)); rng=np.random.default_rng(11)
for n in [4,5,6]:
    p=n*n; t0=time.time()
    res=search(x,n,bounds)
    b=res[0]
    st=[int(b[3][3:])] if b[3].startswith('off') else None
    o=int(b[3][3:]) if b[3].startswith('off') else bounds[0][0]
    seq=b[6]
    dec=''.join(A[i] for k in range(o,min(len(x),o+5*p)-p+1,p) for i in x[k:k+p][seq])
    if b[4]: dec=dec[::-1]
    nul=[search(rng.permutation(x),n,bounds)[0][0] for _ in range(4 if n==6 else 20)]
    print(f'n={n}: best {b[0]:.3f} ccw={b[1]} colmajor={b[2]} {b[3]} rev={b[4]} | nulls max {max(nul):.3f} mean {np.mean(nul):.3f} | {time.time()-t0:.0f}s',flush=True)
    print('   top5 scores',[round(r[0],3) for r in res[:5]],' decryption:',dec[:90],flush=True)
