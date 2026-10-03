import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *; from dewin import *
import numpy as np, glob
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
cnt=Counter()
for f in glob.glob(CORP+'/g*.txt')+glob.glob(CORP+'/p_*.txt'):
    t=gut(open(f,encoding='utf-8',errors='ignore').read()).lower().replace('ß','ss')
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
    cnt.update(re.findall(r'[a-z]+',t))
EXTRA=int(sys.argv[1]) if len(sys.argv)>1 else 2
words=[w for w,c in cnt.most_common(30000) if 4<=len(w)<=9 and all(ch in A for ch in w)][:6000]
print('dictionary',len(words),'extra letters allowed in window:',EXTRA)
M=np.array([[w.count(a) for a in A] for w in words],dtype=np.int16)
lens=np.array([len(w) for w in words])
L=lines_v1(); x=np.array([ix[c] for c in ''.join(''.join(tokens(l,'plain')) for l in L[:-1])]); n=len(x)
onehot=np.eye(26,dtype=np.int16)[x]; cs=np.vstack([np.zeros(26,np.int16),np.cumsum(onehot,0)])
def hits(y):
    oh=np.eye(26,dtype=np.int16)[y]; c=np.vstack([np.zeros(26,np.int16),np.cumsum(oh,0)])
    out=np.zeros(len(words),dtype=np.int32)
    for l in range(4,10):
        sel=np.where(lens==l)[0]
        if len(sel)==0: continue
        W=l+EXTRA; win=(c[W:]-c[:-W])            # (n-W+1) x 26
        fit=(win[:,None,:]>=M[sel][None,:,:]).all(2)   # windows x words
        out[sel]=fit.sum(0)
    return out
obs=hits(x)
rng=np.random.default_rng(1)
NS=int(sys.argv[2]) if len(sys.argv)>2 else 100
nul=np.array([hits(rng.permutation(x)) for _ in range(NS)])
m=nul.mean(0); sd=nul.std(0)+0.5
z=(obs-m)/sd
# global: total hits weighted (sum of z) vs null distribution of sum of z
nz=(nul-m)/sd
tot=z.sum(); tn=nz.sum(1)
print(f'global: sum z real {tot:.1f} | null mean {tn.mean():.1f} sd {tn.std():.1f} -> Z={(tot-tn.mean())/tn.std():+.2f}, p_high={(tn>=tot).mean():.3f}')
# words never/rarely expected but found
frac=(nul>=obs[None,:]).mean(0)
order=np.argsort(frac+ -1e-3*z)
print('words most in excess (obs vs null mean, p_high):')
k=0
for i in order:
    if obs[i]==0: continue
    print(f'  {words[i]:12s} obs {obs[i]:3d} null {m[i]:6.2f} p={frac[i]:.3f}'); k+=1
    if k>=30: break
