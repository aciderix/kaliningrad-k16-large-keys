import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
L=lines_v1()
s=tokens("\n".join(L[:-1]),'plain')
r=tokens("\n".join(L[:-1]),'rich')
random.seed(7)
def rep(seq,d): return sum(seq[i]==seq[i+d] for i in range(len(seq)-d))
def test(seq,name,ds=range(1,13),nsh=4000):
    print(name,len(seq))
    nul={d:[] for d in ds}
    t=seq[:]
    for _ in range(nsh):
        random.shuffle(t)
        for d in ds: nul[d].append(rep(t,d))
    tot_obs=tot_exp=0; 
    for d in ds:
        o=rep(seq,d); m=sum(nul[d])/nsh; sd=(sum((x-m)**2 for x in nul[d])/nsh)**.5
        p=sum(x<=o for x in nul[d])/nsh
        tot_obs+=o; tot_exp+=m
        print(f"  d={d:2d} obs={o:3d} exp={m:6.1f} z={(o-m)/sd:+.2f} p_low={p:.3f}")
    # combined d=1..3
    o=sum(rep(seq,d) for d in (1,2,3)); nn=[sum(nul[d][k] for d in (1,2,3)) for k in range(nsh)]
    m=sum(nn)/nsh; sd=(sum((x-m)**2 for x in nn)/nsh)**.5
    print(f"  d=1..3 combined obs={o} exp={m:.1f} z={(o-m)/sd:+.2f} p_low={sum(x<=o for x in nn)/nsh:.4f}")
test(s,'bottle plain')
test(r,'bottle rich')
# page1 only (reliable)
p1=tokens("\n".join(L[:20]),'plain'); test(p1,'page1 plain',ds=(1,2,3))
# Corsair independent transcription
cs=open(ROOT+'data/transcription_corsair_2015.txt',encoding='utf-8').read().split('\n')
cs=[l for l in cs if not l.startswith('#')][:24]
c=tokens("\n".join(cs),'plain'); test(c,'corsair plain',ds=(1,2,3))
