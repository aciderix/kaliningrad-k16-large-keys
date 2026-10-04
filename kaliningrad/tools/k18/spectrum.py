import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
import numpy as np
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain')
A=sorted(set(s)); idx={a:i for i,a in enumerate(A)}; x=np.array([idx[c] for c in s]); K=len(A)
def mi_d(x,d):
    a=x[:-d]; b=x[d:]; n=len(a)
    M=np.zeros((K,K)); np.add.at(M,(a,b),1)
    pa=M.sum(1); pb=M.sum(0); nz=M>0
    return (M[nz]/n*np.log(M[nz]*n/np.outer(pa,pb)[nz])).sum()
rng=np.random.default_rng(5)
D=range(1,600)
obs=np.array([mi_d(x,d) for d in D])
# null: shuffled, same d's
nul=np.array([[mi_d(y,d) for d in D] for y in (rng.permutation(x) for _ in range(60))])
z=(obs-nul.mean(0))/nul.std(0)
order=np.argsort(-z)[:12]
print('top z distances:',[(list(D)[i],round(z[i],2)) for i in order])
# max z over all d in nulls (family-wise)
nz=(nul-nul.mean(0))/nul.std(0)
print('null max z over 599 distances: mean %.2f, 95%% %.2f'%(nz.max(1).mean(),np.quantile(nz.max(1),.95)))
# control: German text, columnar w=12 (complete) transposition, same length
de=german_corpus()['heldout'][3000:3000+len(s)]
def columnar(t,w,key):
    cols=[t[i::w] for i in range(w)]
    return ''.join(cols[k] for k in key)
key=list(rng.permutation(12)); ct=columnar(de,12,key)
y=np.array([ {c:i for i,c in enumerate(sorted(set(ct)))}[c] for c in ct]); Kc=len(set(ct))
def mi_y(y,d,K):
    a=y[:-d]; b=y[d:]; n=len(a); M=np.zeros((K,K)); np.add.at(M,(a,b),1)
    pa=M.sum(1); pb=M.sum(0); nz=M>0
    return (M[nz]/n*np.log(M[nz]*n/np.outer(pa,pb)[nz])).sum()
o2=np.array([mi_y(y,d,Kc) for d in D]); n2=np.array([[mi_y(rng.permutation(y),d,Kc) for d in D] for _ in range(20)])
z2=(o2-n2.mean(0))/n2.std(0); i2=np.argsort(-z2)[:5]
print('control columnar w=12 top:',[(list(D)[i],round(z2[i],1)) for i in i2],' expected d≈',len(s)//12)
