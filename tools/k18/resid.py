import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain'); N=len(s); bc=Counter(s)
texts=german_corpus(); allde=''.join(texts.values()); ct=Counter(allde); tot=len(allde)
# per-letter: z vs between-window distribution (accounts for overdispersion)
W=[Counter(t[i:i+N]) for t in texts.values() for i in range(0,len(t)-N,N)]
print(f"{'l':2s} {'bottle':>6s} {'DE mean':>7s} {'DE sd':>6s} {'z':>6s}")
rows=[]
for a in 'abcdefghijklmnopqrstuvwxyz':
    v=[w[a] for w in W]; m=sum(v)/len(v); sd=(sum((x-m)**2 for x in v)/len(v))**.5
    rows.append(((bc[a]-m)/sd,a,bc[a],m,sd))
for z,a,b,m,sd in sorted(rows):
    print(f"{a:2s} {b:6d} {m:7.1f} {sd:6.1f} {z:+6.2f}")
# per page / per block z for f, w, n, a
blocks=[]; cur=[]
for line in L[:-1]:
    for w in line.split():
        cur+=tokens(w,'plain')
        if '_' in w: blocks.append(cur); cur=[]
print('blocks',[len(b) for b in blocks],'rest',len(cur))
for a in 'fwnacgb':
    p=ct[a]/tot
    print(a, [round((Counter(b)[a]-len(b)*p)/math.sqrt(len(b)*p*(1-p)),1) for b in blocks])
