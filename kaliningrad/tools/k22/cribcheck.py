import sys, random
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18'))
from common import *
L=lines_v1(); s=''.join(''.join(tokens(l,'plain')) for l in L[:-1]); N=len(s)
def fits(stream,word,W):
    need=Counter(word); n=0
    for a in range(0,len(stream)-W+1):
        c=Counter(stream[a:a+W])
        if all(c[k]>=v for k,v in need.items()): n+=1
    return n/(len(stream)-W+1)
rng=random.Random(1)
shufs=[''.join(rng.sample(s,len(s))) for _ in range(20)]
words=['heimat','pillau','baltijsk','schule','mutter','vater','krieg','freund','liebe','deutschland','russland','flasche','sowjetunion','pionier','geheim','zukunft','kinder','wir','lenin','moskau','kapitan','kompass']
print(f"{'mot':12s} {'fenêtre':>7s} {'bouteille':>9s} {'hasard':>7s}")
for w in words:
    for W in (len(w)+10, len(w)+50):
        fb=fits(s,w,W); fh=sum(fits(x,w,W) for x in shufs)/len(shufs)
        print(f'{w:12s} {W:7d} {fb:9.2f} {fh:7.2f}')
