import os, sys, json, glob; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
L=lines_v1(); rich=tokens("\n".join(L[:-1]),'rich')
fold=lambda s: unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
variants={'plain':Counter(fold(s).replace("'","") for s in rich),
          'accents kept':Counter(s.replace("'","") for s in rich),
          'apostr. distinct':Counter(fold(s) for s in rich),
          'all distinct':Counter(rich)}
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
langs={}
for f in glob.glob(CORP+'/x_*.txt')+glob.glob(CORP+'/en_*.txt')+glob.glob(CORP+'/fr_*.txt'):
    raw=open(f,encoding='utf-8',errors='ignore').read()
    m=re.search(r'^Language:\s*(\w+)',raw,re.M); lang=m.group(1) if m else '?'
    s=''.join(c for c in gut(raw).lower() if c.isalpha() and ord(c)<0x250)
    langs.setdefault(lang,'')
    langs[lang]+=s
langs['German']=''.join(''.join(c for c in gut(open(f,encoding='utf-8',errors='ignore').read()).lower() if c.isalpha() and ord(c)<0x250) for f in glob.glob(CORP+'/g*.txt'))
d=json.load(open(CORP+'/ru_synodal.json',encoding='utf-8-sig'))
langs['Russian (Synodal)']=''.join(c for b in d for ch in b['chapters'] for c in ''.join(ch).lower() if 'а'<=c<='я' or c=='ё')
N=979
def ic(c): n=sum(c.values()); return sum(v*(v-1) for v in c.values())/(n*(n-1))
print('bottle IC:',{k:round(ic(v),4) for k,v in variants.items()})
print(f"{'language':20s} {'IC mean':>8s} {'IC max':>7s} | " + ' | '.join(f'{k:>18s}' for k in variants))
for lang,s in sorted(langs.items()):
    ct=Counter(s); tot=len(s)
    p=sorted([v/tot for v in ct.values()],reverse=True)
    def Gs(counts):
        n=sum(counts); cs=sorted(counts,reverse=True); ps=p+[1e-5]*(len(cs)-len(p))
        return 2*sum(c*math.log(c/(n*q)) for c,q in zip(cs,ps) if c>0)
    W=[Counter(s[i:i+N]) for i in range(0,len(s)-N,N)]
    if len(W)>3000: W=random.Random(1).sample(W,3000)
    gw=[Gs(list(w.values())) for w in W]
    ics=[ic(w) for w in W]
    cells=[]
    for k,c in variants.items():
        g=Gs(list(c.values())); cells.append(f"G={g:6.1f} p={sum(x>=g for x in gw)/len(gw):.4f}")
    print(f"{lang[:20]:20s} {sum(ics)/len(ics):8.4f} {max(ics):7.4f} | "+' | '.join(f'{c:>18s}' for c in cells), len(W))
