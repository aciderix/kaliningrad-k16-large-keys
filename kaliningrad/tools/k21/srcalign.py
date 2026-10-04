import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *; from dewin import *
import numpy as np
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
KEEP=[i for i,a in enumerate(A) if a not in 'fwn']; kmap=-np.ones(26,int); kmap[KEEP]=np.arange(len(KEEP))
W=40
def enc(s): return np.array([ix[c] for c in s])
def reduce(y):  # remove f,w,n ; return indices in reduced alphabet
    r=kmap[y]; return r[r>=0]
def bottle_windows(y):
    r=reduce(y); K=len(r)//W
    return np.stack([np.bincount(r[k*W:(k+1)*W],minlength=len(KEEP)) for k in range(K)]).astype(np.float32)
def scan(src_idx,Bw,step=1):
    r=reduce(src_idx); M=len(r); K=len(Bw)
    if M<K*W+1: return None
    oh=np.zeros((M+1,len(KEEP)),np.float32); oh[np.arange(1,M+1),r]=1; cum=np.cumsum(oh,0)
    betas=np.arange(0,M-K*W,step)
    tot=np.zeros(len(betas),np.float32)
    for k in range(K):
        S=cum[betas+W*(k+1)]-cum[betas+W*k]
        tot+=(((S-Bw[k])**2)/(S+Bw[k]+1)).sum(1)
    return betas,tot
if __name__=='__main__':
    rng=np.random.default_rng(5)
    texts=german_corpus()
    # power check: planted source in Effi Briest
    key=[k for k in texts if 'g5323' in k][0]; src=texts[key]; st=200000
    t=[]
    for c in src[st:st+1300]:
        t.append(c)
        if rng.random()<0.10: t.append('fwn'[rng.integers(3)])
    t=enc(''.join(t[:979])).copy()
    for i in range(0,979,20): t[i:i+20]=rng.permutation(t[i:i+20])
    Bw=bottle_windows(t)
    b,tot=scan(enc(src),Bw)
    j=np.argmin(tot); srt=np.sort(tot)
    # true beta in reduced coordinates
    true_beta=len(reduce(enc(src[:st])))
    print(f'planted: best beta {b[j]} (true {true_beta}) score {tot[j]:.1f} | median {np.median(tot):.1f} | 2nd-best outside ±50: {tot[np.abs(b-b[j])>50].min():.1f} | z_best={(tot[j]-tot.mean())/tot.std():.2f}')
    # same with chunk-60 scramble and 15% nulls
    t=[]
    for c in src[st:st+1400]:
        t.append(c)
        if rng.random()<0.15: t.append('fwn'[rng.integers(3)])
    t=enc(''.join(t[:979])).copy()
    for i in range(0,979,60): t[i:i+60]=rng.permutation(t[i:i+60])
    b,tot=scan(enc(src),bottle_windows(t)); j=np.argmin(tot)
    print(f'planted chunk60/15%: best beta {b[j]} (true {true_beta}) score {tot[j]:.1f} | 2nd outside ±50: {tot[np.abs(b-b[j])>50].min():.1f} | median {np.median(tot):.1f}')
