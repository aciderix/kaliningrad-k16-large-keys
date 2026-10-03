import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *; from dewin import *
L=lines_v1(); s=tokens("\n".join(L[:-1]),'plain'); N=len(s); bc=Counter(s)
texts=german_corpus(keep_umlaut=True)
# sample 3 MB of German (spread across texts)
de=''.join(t[:150000] for t in texts.values())
de=de.replace('ä','ae').replace('ö','oe').replace('ü','ue')  # bottle folds accents; ß kept as 'ss' already
A='abcdefghijklmnopqrstuvwxyz'
def G_of(text,target=bc,n=N):
    c=Counter(text); tot=len(text)
    return 2*sum(target[a]*math.log(target[a]/(n*(c[a]+.5)/(tot+13))) for a in A if target[a]>0)
pats=['sch','ch','ck','ei','ie','au','eu','st','ng','nn','ss','tz','qu','pf','ph','th','v','a','o','c','g','b','k','p','t','h','z','e','i','u','s','d','r','l','m']
repl=list(A)+['']
def greedy(text,target,n,steps=4,verbose=True):
    hist=[]; g0=G_of(text,target,n)
    if verbose: print(f'  start G={g0:.1f}')
    for st in range(steps):
        best=None
        for p in pats:
            if p not in text: continue
            for x in repl:
                if x==p: continue
                g=G_of(text.replace(p,x),target,n)
                if best is None or g<best[0]: best=(g,p,x)
        text=text.replace(best[1],best[2]); hist.append(best)
        if verbose: print(f'  step {st+1}: {best[1]!r} -> {best[2]!r}  G={best[0]:.1f}')
    return text,hist
print('BOTTLE')
t_b,h_b=greedy(de,bc,N)
# typicality: windows of the rewritten German vs its own pool
def window_p(text,target,n):
    c=Counter(text); tot=len(text)
    pr={a:(c[a]+.5)/(tot+13) for a in A}
    Gf=lambda w: 2*sum(w[a]*math.log(w[a]/(n*pr[a])) for a in A if w[a]>0)
    gs=[Gf(Counter(text[i:i+n])) for i in range(0,len(text)-n,n)]
    g=Gf(target); return g,sum(x>=g for x in gs)/len(gs)
print('  bottle vs rewritten German: G=%.1f p=%.4f'%window_p(t_b,bc,N))
# calibration: same greedy for targets = windows of other languages
import glob
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
for f in [CORP+'/x_11024.txt',CORP+'/en_1342.txt',CORP+'/x_218.txt',CORP+'/x_2000.txt',CORP+'/x_11940.txt']:
    raw=open(f,encoding='utf-8',errors='ignore').read()
    t=''.join(c for c in unicodedata.normalize('NFKD',gut(raw).lower()).encode('ascii','ignore').decode() if c in A)
    w=Counter(t[20000:20000+N])
    print('CALIB',f)
    tt,hh=greedy(de,w,N,verbose=False)
    print('   rules',[(p,x) for _,p,x in hh],'G after: %.1f p=%.4f'%window_p(tt,w,N), 'G before %.1f'%G_of(de,w,N))
