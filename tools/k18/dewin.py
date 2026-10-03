import os, sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
import glob
def gut_body(raw):
    a,b=raw.find('*** START'),raw.find('*** END')
    return raw[a+200:b] if 0<a<b else raw
def clean_de(s, keep_umlaut=False):
    s=s.lower().replace('ß','ss')
    if keep_umlaut:
        return ''.join(c for c in s if c in 'abcdefghijklmnopqrstuvwxyzäöü')
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return ''.join(c for c in s if c.isalpha() and c<'{')
def german_corpus(keep_umlaut=False):
    texts={}
    for f in sorted(glob.glob(CORP+'/g*.txt')):
        texts[f]=clean_de(gut_body(open(f,encoding='utf-8',errors='ignore').read()),keep_umlaut)
    texts['heldout']=clean_de(open(ROOT+'data/heldout/de.txt',encoding='utf-8').read(),keep_umlaut)
    return texts
def windows(texts,N=979,step=None):
    step=step or N
    for k,t in texts.items():
        for s in range(0,len(t)-N,step): yield k,t[s:s+N]
