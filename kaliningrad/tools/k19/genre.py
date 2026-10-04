import os, sys, json, glob; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *; from dewin import *
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain'); N=len(s); bc=Counter(s)
A='abcdefghijklmnopqrstuvwxyz'
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
def cl(t): return clean_de(t)
corp={}
for f in sorted(glob.glob(CORP+'/p_*.txt')):
    raw=open(f,encoding='utf-8',errors='ignore').read()
    title=re.search(r'^Title:\s*(.*)',raw,re.M).group(1).strip()[:40]
    corp[title]=cl(gut(raw))
d=json.load(open(CORP+'/de_schlachter.json',encoding='utf-8-sig'))
corp['Bibel (Schlachter 1951)']=cl(' '.join(v for b in d for ch in b['chapters'] for v in ch))
corp['Prosa (21 Bücher)']=''.join(german_corpus().values())
pool=corp['Prosa (21 Bücher)']; ct=Counter(pool); tot=len(pool)
p={a:(ct[a]+.5)/(tot+13) for a in A}
def G1(c): return 2*sum(c[a]*math.log(c[a]/(N*p[a])) for a in A if c[a]>0)
def G2(c1,c2):  # two-sample G (bottle vs window)
    n1=sum(c1.values()); n2=sum(c2.values()); g=0
    for a in A:
        o=[c1[a],c2[a]]; t=sum(o)
        if t==0: continue
        for x,n in zip(o,(n1,n2)):
            e=t*n/(n1+n2)
            if x>0: g+=2*x*math.log(x/e)
    return g
gb=G1(bc)
print(f'bottle: G vs prose pool {gb:.1f}; f+w {bc["f"]+bc["w"]}; n {bc["n"]}; a {bc["a"]}; c {bc["c"]}')
print(f"{'corpus':40s} {'win':>5s} {'f+w med':>7s} {'max':>4s} {'n med':>5s} {'G>=bot':>7s} {'min G2':>7s}")
best=[]
for k,t in corp.items():
    W=[t[i:i+N] for i in range(0,len(t)-N,N//3)]
    if not W: continue
    cs=[Counter(w) for w in W]
    fw=sorted(c['f']+c['w'] for c in cs); nn=sorted(c['n'] for c in cs)
    g1=[G1(c) for c in cs]; g2=[G2(bc,c) for c in cs]
    j=min(range(len(cs)),key=lambda i:g2[i])
    best.append((g2[j],k,W[j][:70]))
    print(f"{k[:40]:40s} {len(W):5d} {fw[len(fw)//2]:7d} {fw[-1]:4d} {nn[len(nn)//2]:5d} {sum(g>=gb for g in g1):7d} {min(g2):7.1f}")
best.sort()
print('closest windows (two-sample G, df=21; 95% crit ~32.7):')
for g,k,w in best[:5]: print(f'  {g:6.1f} {k} :: {w}')
