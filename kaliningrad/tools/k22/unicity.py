import sys, math, random
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *; from dewin import *
texts=german_corpus(); g=''.join(texts.values())[:3000000]
c=Counter(g); tot=len(g); p={a:c[a]/tot for a in c}
H1=-sum(v*math.log2(v) for v in p.values())
rng=random.Random(1)
print(f'entropie d’une lettre isolée (fréquences allemandes) : {H1:.2f} bits')
for n in (3,5,10,25,50,100,170):
    vals=[]
    for _ in range(3000):
        st=rng.randrange(0,tot-n); ch=Counter(g[st:st+n])
        lp=math.lgamma(n+1)-sum(math.lgamma(k+1) for k in ch.values())+sum(k*math.log(p[a]) for a,k in ch.items())
        vals.append(-lp/math.log(2))
    Hc=sum(vals)/len(vals)
    print(f'tranches de {n:3d} lettres : information portée par la composition ≈ {Hc:6.1f} bits par tranche = {Hc/n:.2f} bit par lettre')
