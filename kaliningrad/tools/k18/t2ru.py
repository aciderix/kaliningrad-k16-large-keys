import os, sys, json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
L=lines_v1(); txt="\n".join(L[:-1])
rich=tokens(txt,'rich')
d=json.load(open(CORP+'/ru_synodal.json',encoding='utf-8-sig'))
CY='абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
chapters=[]
for b in d:
    for ch in b['chapters']:
        s=''.join(ch).lower()
        chapters.append((b['id'],''.join(c for c in s if c in CY)))
ru=''.join(c for _,c in chapters)
ct=Counter(ru); tot=len(ru)
print('russian letters',len(ct),[(a,round(100*ct[a]/tot,2)) for a,_ in ct.most_common()])
p=sorted([ct[a]/tot for a in ct],reverse=True)
def Gs(counts):
    N=sum(counts); cs=sorted(counts,reverse=True)
    ps=p+[1e-5]*(len(cs)-len(p))
    return 2*sum(c*math.log(c/(N*q)) for c,q in zip(cs,ps) if c>0)
W=[Counter(ru[s:s+979]) for s in range(0,len(ru)-979,979*3)]
gw=sorted(Gs(list(w.values())) for w in W)
print('windows',len(gw),'median',round(gw[len(gw)//2],1),'max',round(gw[-1],1))
fold=lambda s: unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
for name,f in [('plain',lambda s: fold(s).replace("'","")),('accents kept',lambda s:s.replace("'","")),('apostrophes distinct',fold),('all distinct',lambda s:s)]:
    c=Counter(f(s) for s in rich); g=Gs(list(c.values()))
    print(f"{name:22s} n={len(c)} G={g:7.1f} windows>= {sum(x>=g for x in gw)}/{len(gw)}  top5 {[round(100*v/979,1) for _,v in c.most_common(5)]}")
print('russian top5 %',[round(100*x,1) for x in p[:5]])
# also per chapter (whole chapters, any length) sorted G normalised to N
best=[]
for bid,s in chapters:
    if len(s)<600: continue
    c=Counter(s); N=len(s)
    # compare bottle (apostrophes distinct) proportions with this chapter's sorted proportions via G on bottle counts
    q=sorted([v/N for v in c.values()],reverse=True)
    bc=sorted(Counter(fold(x) for x in rich).values(),reverse=True)
    qq=q+[1e-5]*(len(bc)-len(q))
    g=2*sum(x*math.log(x/(979*y)) for x,y in zip(bc,qq) if x>0)
    best.append((g,bid,N))
best.sort(); print('best chapters (apostrophes distinct):',best[:5])
