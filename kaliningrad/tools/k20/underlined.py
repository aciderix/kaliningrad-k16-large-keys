import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k18')); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k19'))
from common import *
from math import comb
L=lines_v1()
words=[tokens(w,'plain') for l in L[:-1] for w in l.split() if tokens(w,'plain')]
under=[tokens(w,'plain')[-1] for l in L[:-1] for w in l.split() if '_' in w]
fin=Counter(w[-1] for w in words if len(w)>=2); tot=sum(fin.values()); pen=(fin['e']+fin['n'])/tot
stream=''.join(''.join(tokens(l,'plain')) for l in L[:-1]); c=Counter(stream); ps=(c['e']+c['n'])/len(stream)
print('underlined block-final letters:',''.join(under))
print('word-final letters (habillage):',fin.most_common(8),' share e+n = %.3f'%pen, '; stream share e+n = %.3f'%ps)
for p,name in [(ps,'any stream letter'),(pen,'habillage word-final')]:
    print(f'P(>=5 of 6 underlined in {{e,n}}) if like {name}: {sum(comb(6,k)*p**k*(1-p)**(6-k) for k in (5,6)):.4f}')
