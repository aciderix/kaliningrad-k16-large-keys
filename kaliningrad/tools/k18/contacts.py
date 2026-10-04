import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
L=lines_v1(); txt="\n".join(L)
random.seed(1)
for mode in ['plain','rich']:
    s=tokens(txt,mode)
    print(mode,len(s),len(set(s)))
    for d in [1,2,3,4,5]:
        r=mi(s,d); nul=[]
        for _ in range(400):
            t=s[:]; random.shuffle(t); nul.append(mi(t,d))
        m=sum(nul)/len(nul); sd=(sum((x-m)**2 for x in nul)/len(nul))**.5
        print(f"  d={d} MI={r:.4f} null={m:.4f}±{sd:.4f} z={(r-m)/sd:+.2f}")
# German control with same length
de=open(ROOT+'data/heldout/de.txt',encoding='utf-8').read().lower()
de=[c for c in unicodedata.normalize('NFKD',de).encode('ascii','ignore').decode() if c.isalpha()][5000:5979]
r=mi(de,1); nul=[]
for _ in range(200):
    t=de[:]; random.shuffle(t); nul.append(mi(t,1))
m=sum(nul)/len(nul); sd=(sum((x-m)**2 for x in nul)/len(nul))**.5
print('german control d=1 z=',(r-m)/sd)
