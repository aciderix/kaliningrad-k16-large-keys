import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
L=lines_v1()
body=L[:-1]
V=set('aeiouêöü')
# 1. apostrophe bits over consonants
toks=[]
for line in body:
    toks+=tokens(line,'rich')
cons=[t for t in toks if t[0] not in V]
bits=''.join('1' if "'" in t else '0' for t in cons)
print('consonants',len(cons),'apostrophes',bits.count('1'))
# gaps between apostrophes (in consonant units and in letter units)
pos=[i for i,b in enumerate(bits) if b=='1']
gaps=[b-a for a,b in zip(pos,pos[1:])]
print('gap distribution (consonants):',sorted(Counter(gaps).items())[:20])
# Is apostrophe presence predicted by letter identity only? (already: n,t,r,d...). Within n: which n get apostrophes? Check next-letter class
nxt=Counter(); tot=Counter()
for i,t in enumerate(toks[:-1]):
    if t[0]=='n':
        c='V' if toks[i+1][0] in V else 'C'
        tot[c]+=1
        if "'" in t: nxt[c]+=1
print("n followed by V/C: apostrophe rate", {k:(nxt[k],tot[k]) for k in tot})
# position in word: is apostrophe at word end?
wend=Counter(); wall=Counter()
for line in body:
    for w in line.split():
        ts=tokens(w,'rich')
        for j,t in enumerate(ts):
            if t[0] in V: continue
            k='end' if j==len(ts)-1 else 'inner'
            wall[k]+=1
            if "'" in t: wend[k]+=1
print('apostrophe rate by position in word', {k:(wend[k],wall[k],round(wend[k]/wall[k],3)) for k in wall})
# 2. decode bits as 5-bit A=1.. and ASCII
def dec5(b,off):
    out=''
    for i in range(off,len(b)-4,5):
        v=int(b[i:i+5],2); out+=chr(96+v) if 1<=v<=26 else '.'
    return out
for off in range(5): print('5bit off',off,dec5(bits,off)[:80])
# 3. word lengths
wl=[len(tokens(w,'plain')) for line in body for w in line.split() if tokens(w,'plain')]
print('word lengths',wl[:60])
print('wl as letters', ''.join(chr(96+x) if x<=26 else '?' for x in wl))
# 4. line initials / finals
print('line initials', ''.join(tokens(l,'plain')[0] for l in body))
print('line finals  ', ''.join(tokens(l,'plain')[-1] for l in body))
print('letters per line', [len(tokens(l,'plain')) for l in body])
# 5. ê positions: in-word index and neighbours
for line in body:
    for w in line.split():
        if 'ê' in w or 'ö' in w or 'ü' in w: print(w, end='  ')
print()
