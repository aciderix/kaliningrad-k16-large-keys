import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *; from dewin import *
import numpy as np, glob
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
cnt=Counter()
for f in glob.glob(CORP+'/g*.txt'):
    t=gut(open(f,encoding='utf-8',errors='ignore').read()).lower().replace('ß','ss')
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode(); cnt.update(re.findall(r'[a-z]+',t))
DICT=set(w for w,c in cnt.items() if len(w)>=4 and c>=5)
def coverage(s):
    # loc_real_D.out / loc_fake_D.out : sorties de anagram.c (K19) sur les lignes réelles et 10 jeux factices
    # greedy left-to-right: longest dictionary word (>=4) starting at each position
    i=0; cov=0; words=[]
    while i<len(s):
        best=0
        for L in range(min(14,len(s)-i),3,-1):
            if s[i:i+L] in DICT: best=L; break
        if best: cov+=best; words.append(s[i:i+best]); i+=best
        else: i+=1
    return cov/len(s), words
def load(f): return [l.split()[1] for l in open(f)]
for D in (3,5):
    real=load(f'loc_real_{D}.out'); fake=load(f'loc_fake_{D}.out')
    cr=np.mean([coverage(s)[0] for s in real])
    cf=np.array([np.mean([coverage(s)[0] for s in fake[k*25:(k+1)*25]]) for k in range(10)])
    print(f'D={D}: share of letters inside German words (>=4 letters): real {cr:.3f} | fake sets {cf.mean():.3f} ± {cf.std():.3f} (min {cf.min():.3f}, max {cf.max():.3f})')
print('\n--- examples, D=5: REAL lines 11, 14, 25 vs FAKE lines (same positions, set 1) ---')
real=load('loc_real_5.out'); fake=load('loc_fake_5.out')
for i in (10,13,24,3,6):
    print(f'real {i+1:2d}: {real[i]}   words: {" ".join(coverage(real[i])[1])}')
    print(f'fake {i+1:2d}: {fake[i]}   words: {" ".join(coverage(fake[i])[1])}')
