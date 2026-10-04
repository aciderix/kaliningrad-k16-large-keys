import re, struct, math
raw=open('data/transcription_v1.txt',encoding='utf-8').read()
lines=[re.match(r'L\d+\s+(.*)',l).group(1) for l in raw.splitlines() if re.match(r'L\d+\s',l)]
toks=' '.join(lines).split()
q=struct.unpack('<%df'%(26**4),open('data/models/qg_de.bin','rb').read())
tr=str.maketrans('êöü','eou')
def sc(s):
    s=''.join(c for c in s.translate(tr).lower() if c.isalpha() and c.isascii())
    if len(s)<4: return s,None
    v=[q[((ord(s[i])-97)*26**3+(ord(s[i+1])-97)*676+(ord(s[i+2])-97)*26+ord(s[i+3])-97)] for i in range(len(s)-3)]
    return s,sum(v)/len(v)
words=[t for t in toks if not re.fullmatch(r"([a-z]'?\.)+'?",t) and '.' not in t[:-1] or t.endswith('_.')]
abbr=[t for t in toks if re.fullmatch(r"(?:[a-z]'?\.)+'?",t) or t in('c.f.',)]
W=[re.sub(r"[^a-zêöüA]","",t) for t in toks]
W=[w for w in W if w]
seqs={
 'initiales':''.join(w[0] for w in W),
 'finales':''.join(w[-1] for w in W),
 'abréviations':''.join(re.sub(r'[^a-z]','',t) for t in abbr),
 'lettres avant apostrophe':''.join(re.findall(r"([a-zêöü])'",' '.join(lines))),
 'soulignées':''.join(re.findall(r"([a-z])_",' '.join(lines))),
 'longueurs de mots':' '.join(str(len(w)) for w in W),
 'mots d\'1 lettre':''.join(w for w in W if len(w)==1),
 '2es lettres':''.join(w[1] for w in W if len(w)>1),
}
for k,v in seqs.items():
    s,x=sc(v) if k!='longueurs de mots' else (v,None)
    print(f'{k:26s} {("%.2f"%x) if x else "  -  "}  {v[:160]}')
print('abréviations:',abbr)
print('nb mots',len(W))
