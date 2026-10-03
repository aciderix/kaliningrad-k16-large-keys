from periodic import *
rng=np.random.default_rng(13)
Ps=P+P.T
L=lines_v1(); lines=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
x=np.concatenate(lines); n=len(x)
lid=np.concatenate([np.full(len(l),i) for i,l in enumerate(lines)])
def stats(y,D=20):
    w=c=0.0; nw=nc=0
    for d in range(1,D+1):
        same=lid[:-d]==lid[d:]; v=Ps[y[:-d],y[d:]]
        w+=v[same].sum(); nw+=same.sum(); c+=v[~same].sum(); nc+=(~same).sum()
    return w/nw, c/nc
o=stats(x); nul=np.array([stats(rng.permutation(x)) for _ in range(2000)])
z=(np.array(o)-nul.mean(0))/nul.std(0)
print(f'within-line pairs (d<=20): z={z[0]:+.2f} ; cross-line pairs: z={z[1]:+.2f}')
# same with section boundaries instead of lines
s=[]; sid=[]; k=0
for line in L[:-1]:
    for wd in line.split():
        t=tokens(wd,'plain'); sid+= [k]*len(t)
        if '_' in wd: k+=1
sid=np.array(sid)
def stats2(y,ids,D=40):
    w=c=0.0; nw=nc=0
    for d in range(1,D+1):
        same=ids[:-d]==ids[d:]; v=Ps[y[:-d],y[d:]]
        w+=v[same].sum(); nw+=same.sum(); c+=v[~same].sum(); nc+=(~same).sum()
    return w/nw, c/nc
o=stats2(x,sid); nul=np.array([stats2(rng.permutation(x),sid) for _ in range(1000)])
z=(np.array(o)-nul.mean(0))/nul.std(0)
print(f'within-section pairs (d<=40): z={z[0]:+.2f} ; cross-section pairs: z={z[1]:+.2f}')
