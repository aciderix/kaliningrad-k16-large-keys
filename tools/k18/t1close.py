import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain'); N=len(s)
bc=Counter(s)
texts=german_corpus()
allde=''.join(texts.values()); ct=Counter(allde); tot=len(allde)
A='abcdefghijklmnopqrstuvwxyz'
p={a:(ct[a]+.5)/(tot+13) for a in A}
def G(c,n): return 2*sum(c[a]*math.log(c[a]/(n*p[a])) for a in A if c[a]>0)
gb=G(bc,N)
res=[]
for k,t in texts.items():
    for st in range(0,len(t)-N,N//4):
        w=Counter(t[st:st+N]); res.append((G(w,N),w['f']+w['w'],k,st))
res.sort(reverse=True)
print('bottle G',round(gb,1),'f+w',bc['f']+bc['w'],'windows',len(res))
print('windows with G>=bottle:',sum(r[0]>=gb for r in res))
for g,fw,k,st in res[:8]:
    print(round(g,1),fw,k,repr(texts[k][st:st+80]))
fw=sorted(res,key=lambda r:-r[1])[:5]
print('max f+w windows:')
for g,f,k,st in fw: print(f,round(g,1),k,repr(texts[k][st:st+80]))
# per-text G for whole-text profile scaled to N (how far is the whole text from pooled German)
print('per text: f%, w%, n%, a%, o%')
for k,t in texts.items():
    c=Counter(t); n=len(t)
    print(f"{k:20s} f {100*c['f']/n:4.2f} w {100*c['w']/n:4.2f} n {100*c['n']/n:5.2f} a {100*c['a']/n:4.2f} o {100*c['o']/n:4.2f}")
print('bottle',{a:round(100*bc[a]/N,2) for a in 'fwnao'})
