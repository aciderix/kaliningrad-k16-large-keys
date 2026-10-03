import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
import itertools
L=lines_v1(); txt="\n".join(L[:-1])
rich=tokens(txt,'rich')
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
texts={}
for f in sorted(glob.glob(CORP+'/g*.txt')):
    s=gut(open(f,encoding='utf-8',errors='ignore').read()).lower()
    texts[f]=''.join(c for c in s if c in 'abcdefghijklmnopqrstuvwxyzäöüß')
allde=''.join(texts.values()); ct=Counter(allde); tot=len(allde)
p=sorted([ct[a]/tot for a in ct],reverse=True)
print('german alphabet size',len(ct), [ (a,round(100*ct[a]/tot,2)) for a,_ in ct.most_common()])
def Gs(counts):
    N=sum(counts); cs=sorted(counts,reverse=True)
    ps=p+[1e-5]*(len(cs)-len(p))
    return 2*sum(c*math.log(c/(N*q)) for c,q in zip(cs,ps) if c>0)
W=[Counter(t[s:s+979]) for t in texts.values() for s in range(0,len(t)-979,979)]
gw=sorted(Gs(list(w.values())) for w in W)
print('windows',len(gw),'median',round(gw[len(gw)//2],1),'95%',round(gw[int(.95*len(gw))],1),'max',round(gw[-1],1))
fold=lambda s: unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
base=lambda s: fold(s).replace("'","")
def report(name,f):
    c=Counter(f(s) for s in rich); g=Gs(list(c.values()))
    print(f"{name:40s} n={len(c):2d} G={g:6.1f} windows>= {sum(x>=g for x in gw)}/{len(gw)}")
    return g
report('plain', base)
report('ê ö ü kept', lambda s: s.replace("'",""))
report('all modifiers distinct', lambda s: s)
report('apostrophes distinct, accents folded', fold)
# systematic: every subset of apostrophized letters made distinct (accents folded / kept)
aps=['n','t','r','d','f','s','l','m','z']
res=[]
for keep_acc in [False,True]:
    for k in range(0,len(aps)+1):
        for sub in itertools.combinations(aps,k):
            def f(s,sub=sub,keep_acc=keep_acc):
                b=(s if keep_acc else fold(s))
                if "'" in b and b[0] in sub: return b
                return b.replace("'","")
            c=Counter(f(s) for s in rich); g=Gs(list(c.values()))
            res.append((g,keep_acc,sub))
res.sort()
print('best 10 of',len(res))
for g,ka,sub in res[:10]: print(f"  G={g:5.1f} accents_kept={ka} distinct={sub} windows>= {sum(x>=g for x in gw)}/{len(gw)}")
