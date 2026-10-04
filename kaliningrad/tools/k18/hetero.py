import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
L=lines_v1()
blocks=[]; cur=[]
for line in L[:-1]:
    for w in line.split():
        cur+=tokens(w,'plain')
        if '_' in w: blocks.append(cur); cur=[]
s=sum(blocks,[])
A=sorted(set(s))
for i,b in enumerate(blocks):
    c=Counter(b); print(i+1,len(b),' '.join(f"{a}{c[a]}" for a in 'efnwrdatcgbo'))
def chi2(blocks,letters):
    tot=Counter(sum(blocks,[])); N=sum(len(b) for b in blocks); x=0
    for a in letters:
        for b in blocks:
            e=len(b)*tot[a]/N
            if e>0: x+=(Counter(b)[a]-e)**2/e
    return x
def perm_p(stat_fn, nperm=20000):
    obs=stat_fn(blocks); sizes=[len(b) for b in blocks]; t=s[:]; k=0
    for _ in range(nperm):
        random.shuffle(t); bb=[]; i=0
        for z in sizes: bb.append(t[i:i+z]); i+=z
        if stat_fn(bb)>=obs: k+=1
    return obs,k/nperm
random.seed(3)
print('f only: chi2=%.1f p=%.4f'%perm_p(lambda bb: chi2(bb,['f'])))
print('all letters: chi2=%.1f p=%.4f'%perm_p(lambda bb: chi2(bb,A),5000))
# max single-letter chi2 across letters (corrects for picking f)
print('max over letters: chi2=%.1f p=%.4f'%perm_p(lambda bb: max(chi2(bb,[a]) for a in A),5000))
# same statistic for real German: contiguous 6 blocks of same sizes from German texts
texts=german_corpus(); sizes=[len(b) for b in blocks]; N=sum(sizes)
vals=[]; valsall=[]
for t in texts.values():
    for st in range(0,len(t)-N,N):
        seg=list(t[st:st+N]); bb=[]; i=0
        for z in sizes: bb.append(seg[i:i+z]); i+=z
        As=sorted(set(seg))
        vals.append(max(chi2(bb,[a]) for a in As)); valsall.append(chi2(bb,As))
obs=max(chi2(blocks,[a]) for a in A)
print('German contiguous: max-letter chi2 >= bottle: %d/%d ; all-letter chi2 >= bottle %.1f: %d/%d'%(sum(v>=obs for v in vals),len(vals),chi2(blocks,A),sum(v>=chi2(blocks,A) for v in valsall),len(valsall)))
