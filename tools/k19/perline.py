from periodic import *
import itertools, time
def col_perm(Ln,key):
    """columnar: plaintext written in rows of width w, columns read in key order -> returns list: cipher index -> plaintext index"""
    w=len(key); order=[]
    for col in np.argsort(key):
        order+=list(range(col,Ln,w))
    return np.array(order)
def rail_perm(Ln,r):
    if r<2: return np.arange(Ln)
    cyc=2*r-2; rows=[min(i%cyc,cyc-i%cyc) for i in range(Ln)]
    return np.array(sorted(range(Ln),key=lambda i:(rows[i],i)))
def line_score(lines,perms,P_=P):
    tot=0; n=0
    for y,pm in zip(lines,perms):
        pt=np.empty(len(y),dtype=y.dtype); pt[pm]=y   # cipher position i holds plaintext index pm[i]
        tot+=P_[pt[:-1],pt[1:]].sum(); n+=len(y)-1
    return tot/n
def search_lines(lines):
    res=[]
    for w in range(2,9):
        for key in itertools.permutations(range(w)):
            if key[0]!=0 and w>7: pass
            perms=[col_perm(len(y),key) for y in lines]
            for rev in (False,True):
                res.append((line_score(lines,perms,P.T if rev else P),'col',key,rev))
    for r in range(2,9):
        perms=[rail_perm(len(y),r) for y in lines]
        for rev in (False,True): res.append((line_score(lines,perms,P.T if rev else P),'rail',r,rev))
    res.append((line_score(lines,[np.arange(len(y)) for y in lines],P.T),'reverse',0,True))
    res.sort(key=lambda t:-t[0]); return res
if __name__=='__main__':
    rng=np.random.default_rng(3)
    L=lines_v1(); lines=[enc(''.join(tokens(l,'plain'))) for l in L[:-1]]
    t0=time.time(); res=search_lines(lines); print('real top:',[(round(r[0],3),r[1],r[2],r[3]) for r in res[:3]],f'{time.time()-t0:.0f}s',flush=True)
    # control: German lines of same lengths, columnar key w=6
    ho=german_corpus()['heldout']; st=5000; cl=[]
    key=tuple(rng.permutation(6))
    for y in lines:
        pt=enc(ho[st:st+len(y)]); st+=len(y); pm=col_perm(len(y),key); c=pt[pm]; cl.append(c)
    rc=search_lines(cl); print('control col w=6 key',key,'top:',[(round(r[0],3),r[1],r[2],r[3]) for r in rc[:2]],flush=True)
    # null
    x=np.concatenate(lines); nm=[]
    for k in range(5):
        y=rng.permutation(x); ls=[]; i=0
        for l in lines: ls.append(y[i:i+len(l)]); i+=len(l)
        nm.append(search_lines(ls)[0][0])
    print('nulls best:',[round(v,3) for v in nm],flush=True)
