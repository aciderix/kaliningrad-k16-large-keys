import os, sys; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from periodic import *
rng=np.random.default_rng(9)
Ps=P+P.T
VOW=set(ix[c] for c in 'aeiou')
L=lines_v1(); letters=[]; wid=[]; k=0
for line in L[:-1]:
    for w in line.split():
        t=tokens(w,'plain')
        if t: letters+=t; wid+=[k]*len(t); k+=1
x=enc(''.join(letters)); wid=np.array(wid); n=len(x)
# empirical cut model: P(cut after position i | class pair, current word length bucket)
def cls(a,b): return (a in VOW)*2+(b in VOW)
cnt=np.zeros((4,9)); cut=np.zeros((4,9)); cur=1
for i in range(n-1):
    c=cls(x[i],x[i+1]); lb=min(cur,8); cnt[c,lb]+=1
    if wid[i]!=wid[i+1]: cut[c,lb]+=1; cur=1
    else: cur+=1
pc=(cut+0.5)/(cnt+1)
def resegment(y):
    w=np.zeros(n,int); cur=1; k=0
    for i in range(n-1):
        if rng.random()<pc[cls(y[i],y[i+1]),min(cur,8)]: k+=1; cur=1
        else: cur+=1
        w[i+1]=k
    return w
def stat(y,w,D=4):
    r=[]
    for same in (True,False):
        num=den=0
        for d in range(1,D+1):
            m=(w[:-d]==w[d:]) if same else (w[:-d]!=w[d:]); v=Ps[y[:-d],y[d:]]; num+=v[m].sum(); den+=m.sum()
        r.append(num/den)
    return r
o=stat(x,wid)
nul=[]
for _ in range(1500):
    y=rng.permutation(x); nul.append(stat(y,resegment(y)))
nul=np.array(nul)
for j,name in enumerate(['paires dans un même mot','paires entre deux mots']):
    print(f'{name:26s}: z={(o[j]-nul[:,j].mean())/nul[:,j].std():+.2f} (témoin : flux mélangé redécoupé par la même règle)')
