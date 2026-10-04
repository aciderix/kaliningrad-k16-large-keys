import os, sys, json, glob; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *; from dewin import *
import numpy as np
A='abcdefghijklmnopqrstuvwxyz'; ix={a:i for i,a in enumerate(A)}
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
def fold(s):
    s=s.lower().replace('ß','ss'); s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return ''.join(c for c in s if c in A)
langs={}
for f in glob.glob(CORP+'/x_*.txt')+glob.glob(CORP+'/en_*.txt')+glob.glob(CORP+'/fr_*.txt')+glob.glob(CORP+'/p_*.txt'):
    raw=open(f,encoding='utf-8',errors='ignore').read()
    m=re.search(r'^Language:\s*(\w+)',raw,re.M); lang=m.group(1) if m else '?'
    t=re.search(r'^Title:\s*(.*)',raw,re.M).group(1)
    if 'Plattdeutsch' in t: lang='LowGerman'
    if 'Pennsylvan' in t: lang='PennsylvaniaGerman'
    if os.path.basename(f).startswith('p_'): 
        if lang=='German': lang='GermanPoetry'
    langs[lang]=langs.get(lang,'')+fold(gut(raw))
langs['German']=''.join(german_corpus().values())
ru=json.load(open(CORP+'/ru_synodal.json',encoding='utf-8-sig'))
rus=''.join(c for b in ru for ch in b['chapters'] for c in ' '.join(ch).lower())
tr_de={'а':'a','б':'b','в':'w','г':'g','д':'d','е':'e','ё':'jo','ж':'sch','з':'s','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'ch','ц':'z','ч':'tsch','ш':'sch','щ':'schtsch','ъ':'','ы':'y','ь':'','э':'e','ю':'ju','я':'ja'}
tr_sci={'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'z','з':'z','и':'i','й':'j','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'c','ч':'c','ш':'s','щ':'s','ъ':'','ы':'y','ь':'','э':'e','ю':'ju','я':'ja'}
langs['Russian(de-translit)']=''.join(tr_de.get(c,'') for c in rus)[:3000000]
langs['Russian(sci-translit)']=''.join(tr_sci.get(c,'') for c in rus)[:3000000]
L=lines_v1(); x=np.array([ix[c] for c in ''.join(''.join(tokens(l,'plain')) for l in L[:-1])])
rng=np.random.default_rng(3)
shuf=[rng.permutation(x) for _ in range(800)]
print(f"{'model':24s} {'z d1-10':>8s} {'z d1-2':>7s}  (in-order own-language control z d1-10)")
for name,t in sorted(langs.items()):
    if len(t)<50000: continue
    arr=np.frombuffer(t.encode(),dtype=np.uint8)-97
    B=np.full((26,26),0.5); u=np.full(26,0.5); np.add.at(B,(arr[:-1],arr[1:]),1); np.add.at(u,arr,1)
    P=np.log(B/B.sum(1,keepdims=True))-np.log(u/u.sum())[None,:]; Ps=P+P.T
    band=lambda y,a,b: np.mean([Ps[y[:-d],y[d:]].mean() for d in range(a,b+1)])
    res=[]
    for a,b in [(1,10),(1,2)]:
        o=band(x,a,b); nb=np.array([band(y,a,b) for y in shuf]); res.append((o-nb.mean())/nb.std())
    print(f"{name:24s} {res[0]:+8.2f} {res[1]:+7.2f}")
