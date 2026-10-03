# word unigram/bigram counts from German books, EXCLUDING Kafka (used for controls)
import re, glob, unicodedata, pickle, collections
import os
K=os.environ.get('K18_CORPUS','corpus').rstrip('/')+'/../'  # dossier contenant corp/ (corpus K18) et gut/ (Gutenberg allemand)
def gut(raw):
    a,b=raw.find('*** START'),raw.find('*** END'); return raw[a+200:b] if 0<a<b else raw
def norm(t):
    t=t.lower().replace('ß','ss'); t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
    return re.findall(r'[a-z]+',t)
files=[f for f in glob.glob(K+'corp/g*.txt') if 'g22367' not in f]
files+=sorted(glob.glob(K+'gut/t_*.txt'))[:400]
uni=collections.Counter(); bi=collections.Counter(); ntok=0
for f in files:
    w=norm(gut(open(f,encoding='utf-8',errors='ignore').read()))
    uni.update(w); bi.update(zip(w,w[1:])); ntok+=len(w)
print('files',len(files),'tokens',ntok,'types',len(uni))
vocab={w:c for w,c in uni.items() if c>=3 and len(w)<=16}
bi={k:v for k,v in bi.items() if v>=2 and k[0] in vocab and k[1] in vocab}
print('vocab',len(vocab),'bigrams',len(bi))
pickle.dump((vocab,bi,ntok),open('lm.pkl','wb'))
