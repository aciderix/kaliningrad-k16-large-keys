from periodic import *
import itertools, time
def orbits(n):
    seen=set(); orb=[]; center=None
    for r in range(n):
        for c in range(n):
            if (r,c) in seen: continue
            o=[]; rr,cc=r,c
            for k in range(4):
                o.append(rr*n+cc); seen.add((rr,cc)); rr,cc=cc,n-1-rr   # clockwise rotation of cell position
            if len(set(o))==1: center=o[0]
            else: orb.append(o)
    return orb,center
def all_sequences(n,ccw=False):
    """decryption read order (cell indices) for every grille: array (4^k, n*n)"""
    orb,center=orbits(n); k=len(orb)
    O=np.array(orb)                       # k x 4, O[j,r] = cell of orbit j after r cw rotations from its rep
    if ccw: O=O[:,[0,3,2,1]]
    choices=np.array(list(itertools.product(range(4),repeat=k)),dtype=np.int8)  # 4^k x k
    seqs=[]
    for r in range(4):
        cells=O[np.arange(k)[None,:],(choices+r)%4]   # 4^k x k
        cells.sort(axis=1)
        seqs.append(cells)
        if center is not None and r==0:
            seqs.append(np.full((len(choices),1),center))
    return np.concatenate(seqs,axis=1), choices
def colmajor(seq,n):
    r,c=seq//n,seq%n; return c*n+r
def score_all(seqs,S,Sw):
    sc=S[seqs[:,:-1],seqs[:,1:]].sum(1)+Sw[seqs[:,-1],seqs[:,0]]
    return sc
def scores_for(x,n,starts,P_):
    p=n*n
    S=np.zeros((p,p)); Sw=np.zeros((p,p)); nb=0
    for st in starts:
        g=x[st:st+p]; S+=P_[g[:,None],g[None,:]]; nb+=1
    for a,b in zip(starts,starts[1:]):
        if b==a+p: Sw+=P_[x[a:a+p][:,None],x[b:b+p][None,:]]
    return S,Sw,nb*(p-1)+len(starts)-1
def search(x,n,bounds=None,offsets=None,verbose=False):
    best=[]
    p=n*n
    for ccw in (False,True):
        seqs0,ch=all_sequences(n,ccw)
        for cm in (False,True):
            seqs=colmajor(seqs0,n) if cm else seqs0
            aligns=[]
            for off in (offsets if offsets is not None else range(p)):
                aligns.append(('off%d'%off,list(range(off,len(x)-p+1,p))))
            if bounds:
                st=[]
                for a,b in bounds: st+=list(range(a,b-p+1,p))
                aligns.append(('sections',st))
            for name,st in aligns:
                for rev in (False,True):
                    P_=P.T if rev else P
                    S,Sw,nbig=scores_for(x,n,st,P_)
                    sc=score_all(seqs,S,Sw)/nbig
                    j=int(np.argmax(sc)); best.append((float(sc[j]),ccw,cm,name,rev,j,seqs[j]))
    best.sort(key=lambda t:-t[0])
    return best
