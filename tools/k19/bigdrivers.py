from periodic import *
L=lines_v1(); s=[]
for line in L[:-1]:
    for w in line.split(): s+=tokens(w,'plain')
x=enc(''.join(s)); n=len(x); rng=np.random.default_rng(2)
V=set(ix[c] for c in 'aeiou')
# pair counts within distance 1..10 (unordered), observed vs expected under shuffle
cnt=np.zeros((26,26))
for d in range(1,11):
    np.add.at(cnt,(x[:-d],x[d:]),1)
cs=cnt+cnt.T
f=np.bincount(x,minlength=26)/n
tot=cnt.sum()
exp=np.outer(f,f)*tot*2
Ps=P+P.T
contrib=(cs-exp)*Ps/2
idx=np.dstack(np.unravel_index(np.argsort(-contrib.ravel()),(26,26)))[0]
seen=set(); print('top positive contributors (pair, obs, exp, Ps):')
k=0
for i,j in idx:
    if (j,i) in seen or i>j: continue
    seen.add((i,j)); print(f'  {A[i]}{A[j]} obs={cs[i,j]:.0f} exp={exp[i,j]:.1f} Ps={Ps[i,j]:+.2f} contrib={contrib[i,j]:+.1f}'); k+=1
    if k>=15: break
# V/C alternation at distances 1..10
for d in range(1,11):
    a=np.array([c in V for c in x[:-d]]); b=np.array([c in V for c in x[d:]])
    alt=(a!=b).sum()
    nul=[]
    for _ in range(500):
        y=rng.permutation(x); aa=np.array([c in V for c in y[:-d]]); bb=np.array([c in V for c in y[d:]]); nul.append((aa!=bb).sum())
    print(f'd={d} VC alternations {alt} null {np.mean(nul):.1f}±{np.std(nul):.1f} z={(alt-np.mean(nul))/np.std(nul):+.2f}')
