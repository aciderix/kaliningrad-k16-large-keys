import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain')
random.seed(11)
def gapdisp(seq):
    # mean over letters with >=8 occurrences of (var/mean^2) of gaps
    pos={}
    for i,c in enumerate(seq): pos.setdefault(c,[]).append(i)
    vals=[]
    for c,p in pos.items():
        if len(p)<8: continue
        g=[b-a for a,b in zip(p,p[1:])]; m=sum(g)/len(g); v=sum((x-m)**2 for x in g)/len(g)
        vals.append(v/m/m)
    return sum(vals)/len(vals)
def alphpairs(seq):
    return sum(1 for a,b in zip(seq,seq[1:]) if ord(b)-ord(a) in (1,-1))
def fwd(seq): return sum(1 for a,b in zip(seq,seq[1:]) if ord(b)-ord(a)==1)
for name,f in [('gap dispersion (low = cycling)',gapdisp),('alphabet-adjacent pairs',alphpairs),('forward alphabet pairs (ab,bc..)',fwd)]:
    o=f(s); t=s[:]; nul=[]
    for _ in range(3000):
        random.shuffle(t); nul.append(f(t))
    m=sum(nul)/len(nul); sd=(sum((x-m)**2 for x in nul)/len(nul))**.5
    print(f"{name:36s} obs={o:.3f} null={m:.3f}±{sd:.3f} z={(o-m)/sd:+.2f} p_low={sum(x<=o for x in nul)/len(nul):.3f} p_high={sum(x>=o for x in nul)/len(nul):.3f}")
# same stats on a transposed German control (shuffled German window) for reference: by construction null-like
