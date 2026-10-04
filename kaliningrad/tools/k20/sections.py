import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(31)
Ps=P+P.T
L=lines_v1(); s=[]; sid=[]; k=0
for line in L[:-1]:
    for w in line.split():
        t=tokens(w,'plain'); s+=t; sid+=[k]*len(t)
        if '_' in w: k+=1
x=enc(''.join(s)); sid=np.array(sid); n=len(x)
bnd=np.where(np.diff(sid)!=0)[0]+1   # first index of each new section
print('section starts',bnd)
# statistic: mean Ps over pairs (i,j), |i-j|<=D, that straddle a section boundary, vs. same for pseudo-boundaries
D=12
def straddle_score(y,cuts):
    tot=0; cnt=0
    for b in cuts:
        for i in range(max(0,b-D),b):
            for j in range(b,min(n,i+D+1)):
                tot+=Ps[y[i],y[j]]; cnt+=1
    return tot/cnt
def within_score(y,cuts):
    tot=0; cnt=0
    for b in cuts:
        for i in range(max(0,b-2*D),b-D):   # pairs on the same side just before the boundary
            for j in range(i+1,min(b,i+D+1)):
                tot+=Ps[y[i],y[j]]; cnt+=1
    return tot/cnt
real_s=straddle_score(x,bnd); real_w=within_score(x,bnd)
ns=[]; nw=[]
for _ in range(2000):
    y=rng.permutation(x); ns.append(straddle_score(y,bnd)); nw.append(within_score(y,bnd))
ns=np.array(ns); nw=np.array(nw)
print(f'pairs straddling the 5 section boundaries (d<={D}): z={(real_s-ns.mean())/ns.std():+.2f}')
print(f'pairs just before boundaries, same side:          z={(real_w-nw.mean())/nw.std():+.2f}')
# same statistic at 200 random pseudo-boundaries (positions), to calibrate what a non-boundary gives
pseudo=[]
for _ in range(300):
    cuts=np.sort(rng.choice(np.arange(30,n-30),5,replace=False))
    pseudo.append((straddle_score(x,cuts)-ns.mean())/ns.std())
pseudo=np.array(pseudo)
print(f'straddling random pseudo-boundaries in the real text: z mean {pseudo.mean():+.2f} sd {pseudo.std():.2f}; real boundaries rank p_low={(pseudo<=(real_s-ns.mean())/ns.std()).mean():.3f}')
