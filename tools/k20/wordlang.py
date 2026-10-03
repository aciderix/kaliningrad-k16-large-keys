import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
import json, glob
from common import *; from dewin import *
import numpy as np
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
def fold(t):
    t=t.lower().replace('ß','ss'); return unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
def words_of(text): return re.findall(r'[a-z]+',text)
src={}
def add(lang,text): src.setdefault(lang,Counter()).update(words_of(fold(text)))
for f in glob.glob(CORP+'/g*.txt'): add('German',gut(open(f,encoding='utf-8',errors='ignore').read()))
for f in glob.glob(CORP+'/p_*.txt')+glob.glob(CORP+'/x_*.txt')+glob.glob(CORP+'/en_*.txt')+glob.glob(CORP+'/fr_*.txt'):
    raw=open(f,encoding='utf-8',errors='ignore').read()
    lang=re.search(r'^Language:\s*(\w+)',raw,re.M).group(1); t=re.search(r'^Title:\s*(.*)',raw,re.M).group(1)
    if 'Plattdeutsch' in t: lang='LowGerman'
    elif 'Pennsylvan' in t: lang='PennsylvaniaGerman'
    elif lang=='German': lang='GermanPoetry'
    add(lang,gut(raw))
ru=json.load(open(CORP+'/ru_synodal.json',encoding='utf-8-sig'))
tr={'а':'a','б':'b','в':'w','г':'g','д':'d','е':'e','ё':'jo','ж':'sch','з':'s','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'ch','ц':'z','ч':'tsch','ш':'sch','щ':'schtsch','ъ':'','ы':'y','ь':'','э':'e','ю':'ju','я':'ja'}
rus=' '.join(' '.join(ch) for b in ru for ch in b['chapters']).lower()
add('Russian(de-translit)',''.join(tr.get(c,' ' if not c.isalpha() else '') for c in rus))
L=lines_v1(); x=np.array([ix[c] for c in ''.join(''.join(tokens(l,'plain')) for l in L[:-1])])
rng=np.random.default_rng(1); NS=120; nulls=[rng.permutation(x) for _ in range(NS)]
EXTRA=5
def hits(y,M,lens):
    oh=np.eye(26,dtype=np.int16)[y]; c=np.vstack([np.zeros(26,np.int16),np.cumsum(oh,0)]); out=np.zeros(len(lens),dtype=np.int32)
    for l in range(4,10):
        sel=np.where(lens==l)[0]
        if len(sel)==0: continue
        W=l+EXTRA; win=(c[W:]-c[:-W]); out[sel]=(win[:,None,:]>=M[sel][None,:,:]).all(2).sum(0)
    return out
for lang,cnt in sorted(src.items()):
    ws=[w for w,_ in cnt.most_common(40000) if 4<=len(w)<=9][:3000]
    if len(ws)<1000: continue
    M=np.array([[w.count(a) for a in A] for w in ws],dtype=np.int16); lens=np.array([len(w) for w in ws])
    obs=hits(x,M,lens); nul=np.array([hits(y,M,lens) for y in nulls]); m=nul.mean(0); sd=nul.std(0)+0.5
    tot=((obs-m)/sd).sum(); tn=((nul-m)/sd).sum(1)
    print(f'{lang:22s} words={len(ws)} Z={(tot-tn.mean())/tn.std():+.2f} p_high={(tn>=tot).mean():.3f}',flush=True)
