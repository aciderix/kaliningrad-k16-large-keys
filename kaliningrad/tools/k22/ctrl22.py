import os
import sys, random, re, unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wdecode import Decoder
import os
K=os.environ.get('K18_CORPUS','corpus').rstrip('/')+'/../'  # dossier contenant corp/ (corpus K18) et gut/ (Gutenberg allemand)
raw=open(K+'corp/g22367.txt',encoding='utf-8').read()
raw=raw[raw.find('*** START')+200:]
t=raw.lower().replace('ß','ss'); t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
words=re.findall(r'[a-z]+',t)
s=int(sys.argv[1]); L=int(sys.argv[2]); beam=int(sys.argv[3]); start=int(sys.argv[4]) if len(sys.argv)>4 else 3000
rng=random.Random(s*100+start)
ws=[]; n=0; k=start
while n<L: ws.append(words[k]); n+=len(words[k]); k+=1
plain=''.join(ws)
keys=[i+rng.uniform(0,s) for i in range(len(plain))]
cipher=''.join(plain[i] for i in sorted(range(len(plain)),key=lambda i:keys[i]))
dec=Decoder()
D=s+3
res=dec.decode(cipher,D,beam=beam,verbose=False)
out=''.join(res[1]) if res else ''
acc=sum(a==b for a,b in zip(out,plain))/len(plain)
truew=set((i,w) for i,w in enumerate(ws))
print(f's={s} L={len(plain)} beam={beam} D={D} | letter accuracy {acc:.2f}')
print(' TRUE:',' '.join(ws))
print(' DEC :',' '.join(res[1]) if res else None)
import math
print(' score dec %.1f'%res[0] if res else '', '| score true %.1f'%sum(dec.wscore(p,w) if w in dec.vocab else -99 for p,w in zip([None]+ws[:-1],ws)))
