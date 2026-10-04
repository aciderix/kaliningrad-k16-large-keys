import os
import re, unicodedata, math, random
from collections import Counter
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/'
CORP=os.environ.get('K18_CORPUS','corpus')
def lines_v1(path=ROOT+'data/transcription_v1.txt'):
    src=open(path,encoding='utf-8').read()
    return [re.match(r"L\d+\s+(.*)",l).group(1) for l in src.splitlines() if re.match(r"L\d+\s",l)]
def tokens(text, mode='plain'):
    """mode plain: letters only, accents folded. 'rich': letter+modifiers as symbols (n' , ê, ö, ü distinct)."""
    out=[]
    t=text
    i=0
    while i<len(t):
        ch=t[i]
        if ch.isalpha():
            sym=ch.lower()
            if mode=='plain':
                sym=unicodedata.normalize('NFKD',sym).encode('ascii','ignore').decode()
            j=i+1
            if mode=='rich':
                while j<len(t) and t[j] in "'\"": sym+="'"; j+=1
            out.append(sym); i=j
        else: i+=1
    return out
def mi(seq, d=1):
    pairs=Counter(zip(seq,seq[d:])); n=sum(pairs.values())
    a=Counter(x for x,_ in pairs); b=Counter(y for _,y in pairs)
    return sum(c/n*math.log(c*n/(a[x]*b[y])) for (x,y),c in pairs.items())
