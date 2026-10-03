import os, sys, subprocess, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *; from dewin import *
AN=os.environ.get('K19_ANAGRAM','./anagram')
Q=os.path.join(ROOT,'data/models/qg_de.bin')
rng=np.random.default_rng(8)
ho=german_corpus()['heldout']; L=lines_v1(); sizes=[len(''.join(tokens(l,'plain'))) for l in L[:-1]]
def run(lines,D,seed):
    out=subprocess.run([AN,Q,'6','200000',str(seed),str(D)],input='\n'.join(lines)+'\n',capture_output=True,text=True).stdout
    return np.array([float(l.split()[0]) for l in out.strip().split('\n')])
def make(kind,k):
    st=int(rng.integers(0,len(ho)-30000)); text=ho[st:st+sum(sizes)+50]
    # add 10% nulls f/w/n to mimic bottle composition
    t=[]
    for c in text:
        t.append(c)
        if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
    t=np.array(t[:sum(sizes)])
    if kind=='chunk':
        for i in range(0,len(t),k): t[i:i+k]=rng.permutation(t[i:i+k])
    elif kind=='jitter':
        t=t[np.argsort(np.arange(len(t))+rng.uniform(0,k,len(t)))]
    s=''.join(t); lines=[]; i=0
    for z in sizes: lines.append(s[i:i+z]); i+=z
    return lines
def fakes(lines,nset=6):
    x=''.join(lines); out=[]
    for _ in range(nset):
        y=''.join(rng.permutation(list(x))); ls=[]; i=0
        for z in sizes: ls.append(y[i:i+z]); i+=z
        out.append(ls)
    return out
for kind,k in [('chunk',4),('chunk',6),('chunk',10),('chunk',20),('chunk',40),('jitter',4),('jitter',8),('jitter',16),('none',0)]:
    lines=make(kind,k); F=fakes(lines)
    zs=[]
    for D in (3,5,10,20):
        r=run(lines,D,1).mean(); f=np.array([run(ls,D,2+j).mean() for j,ls in enumerate(F)])
        zs.append((r-f.mean())/f.std())
    print(f'{kind:6s} k={k:2d}  z(D=3,5,10,20): '+' '.join(f'{z:+6.1f}' for z in zs),flush=True)
print('bottle         z(D=3,5,10,20):   +5.3   +4.8   +2.7   +2.9')
