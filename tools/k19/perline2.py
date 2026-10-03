from perline import *
from math import gcd
def decim_perm(Ln,k,s):
    # cipher i takes plaintext index (s + i*k) mod Ln  (needs gcd(k,Ln)=1)
    return np.array([(s+i*k)%Ln for i in range(Ln)])
def ends_perm(Ln,mode):
    idx=list(range(Ln)); out=[]
    lo,hi=0,Ln-1; t=0
    while lo<=hi:
        if (t%2==0)==(mode=='first'): out.append(lo); lo+=1
        else: out.append(hi); hi-=1
        t+=1
    if mode=='inside': out=out[::-1]
    return np.array(out)
def search2(lines):
    res=[]
    for k in range(2,16):
        for s in range(0,1):
            perms=[]; ok=True
            for y in lines:
                if gcd(k,len(y))!=1: perms.append(None)
                else: perms.append(decim_perm(len(y),k,s))
            use=[(y,p) for y,p in zip(lines,perms) if p is not None]
            if len(use)<10: continue
            for rev in (False,True):
                res.append((line_score([u[0] for u in use],[u[1] for u in use],P.T if rev else P),'decim',k,rev,len(use)))
    for mode in ('first','last','inside'):
        perms=[ends_perm(len(y),mode) for y in lines]
        for rev in (False,True): res.append((line_score(lines,perms,P.T if rev else P),'ends',mode,rev,len(lines)))
    res.sort(key=lambda t:-t[0]); return res
rng=np.random.default_rng(5)
L=lines_v1(); lines=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
r=search2(lines); print('real top:',[(round(a,3),b,c,d,e) for a,b,c,d,e in r[:4]])
ho=german_corpus()['heldout']; st=9000; cl=[]
for y in lines:
    pt=enc(ho[st:st+len(y)]); st+=len(y); pm=ends_perm(len(y),'last'); cl.append(pt[pm])
print('control ends/last:',[(round(a,3),b,c,d) for a,b,c,d,e in search2(cl)[:2]])
x=np.concatenate(lines); nm=[]
for _ in range(10):
    y=rng.permutation(x); ls=[]; i=0
    for l in lines: ls.append(y[i:i+len(l)]); i+=len(l)
    nm.append(search2(ls)[0][0])
print('nulls best:',[round(v,3) for v in nm])
