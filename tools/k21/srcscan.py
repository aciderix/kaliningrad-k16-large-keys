import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
import glob, json
from srcalign import *
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
def fold(t):
    t=t.lower().replace('ß','ss'); t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode(); return ''.join(c for c in t if c in A)
L=lines_v1(); x=enc(''.join(''.join(tokens(l,'plain')) for l in L[:-1])); Bw=bottle_windows(x)
print('bottle reduced windows:',len(Bw),'x',W)
files=sys.argv[1:] if len(sys.argv)>1 else sorted(glob.glob(CORP+'/*.txt'))
rows=[]
for f in files:
    raw=open(f,encoding='utf-8',errors='ignore').read()
    t=fold(gut(raw))
    if len(t)<2000: continue
    r=scan(enc(t),Bw,step=1)
    if r is None: continue
    b,tot=r; j=np.argmin(tot)
    rows.append((tot[j],f,int(b[j]),float(np.median(tot)),len(t)))
for f in [CORP+'/ru_synodal.json',CORP+'/de_schlachter.json']:
    try:
        d=json.load(open(f,encoding='utf-8-sig'))
        t=' '.join(' '.join(ch) for b in d for ch in b['chapters'])
        if 'ru_' in f:
            tr={'а':'a','б':'b','в':'w','г':'g','д':'d','е':'e','ё':'jo','ж':'sch','з':'s','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'ch','ц':'z','ч':'tsch','ш':'sch','щ':'schtsch','ъ':'','ы':'y','ь':'','э':'e','ю':'ju','я':'ja'}
            t=''.join(tr.get(c,'') for c in t.lower())
        t=fold(t); b,tot=scan(enc(t),Bw); j=np.argmin(tot); rows.append((tot[j],f,int(b[j]),float(np.median(tot)),len(t)))
    except FileNotFoundError: pass
rows.sort()
for s,f,b,med,n in rows[:12]: print(f'{s:7.1f}  median {med:6.1f}  len {n:8d}  {f}  beta={b}')
print('(planted-source controls: 21.7 ; 65.5 with chunk-60 + 15% nulls ; unrelated text best ≈ 140-150)')
