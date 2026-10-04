"""Clés-phrases tirées d'un dump Wikiquote (pour les attaques par dictionnaire de double transposition).
Lit le dump .xml.bz2, extrait les citations, et écrit les clés (lettres a–z, accents repliés) d'une tranche :
  prefix  : débuts de phrase en mots entiers, longueur lo..hi
  trunc   : lo..hi premières lettres de la phrase (coupure n'importe où)
  windows : toute suite de mots entiers de longueur lo..hi
Répartition sans doublon entre tranches : une clé va dans la tranche crc32(clé) mod N.
Usage : python3 phrasekeys.py dump.xml.bz2 lo hi modes(p.ex. prefix,trunc) tranche N sortie.txt"""
import bz2, re, sys, unicodedata, zlib
dump, lo, hi, modes, shard, N, out_f = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(','), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
TEMPL = re.compile(r'\{\{[^{}]*\}\}'); LINK = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]')
EXT = re.compile(r'\[https?://\S+\s*([^\]]*)\]'); QUOTE = re.compile(r"'{2,}"); TAG = re.compile(r'<[^>]+>')
def clean(s):
    for _ in range(3): s = TEMPL.sub('', s)
    s = LINK.sub(r'\1', s); s = EXT.sub(r'\1', s); s = QUOTE.sub('', s); s = TAG.sub('', s)
    return s.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
def sentences():
    intext = False
    with bz2.open(dump, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if '<text' in line: intext = True
            if intext:
                s = line
                if s.lstrip().startswith(('*', ':')) or (s.strip() and not s.lstrip().startswith(('{', '|', '!', '=', '[[Category', '<'))):
                    t = clean(s.lstrip('*: \t#')).strip()
                    if len(t) > 15 and not t.startswith(('http', 'File:', 'Image:')):
                        for sent in re.split(r'(?<=[.!?;:])\s+', t):
                            sent = sent.strip(' "“”‘’\'()-—–')
                            if sum(c.isalpha() for c in sent) >= 12: yield sent
            if '</text>' in line: intext = False
seen = set(); out = open(out_f, 'w'); n = 0
for sent in sentences():
    t = unicodedata.normalize('NFKD', sent.lower().replace('ß', 'ss')).encode('ascii', 'ignore').decode()
    words = [w for w in (re.sub('[^a-z]', '', x) for x in t.split()) if w]
    if not words: continue
    cands = []
    if 'prefix' in modes:
        acc = ''
        for w in words:
            acc += w
            if len(acc) > hi: break
            if len(acc) >= lo: cands.append(acc)
    if 'trunc' in modes:
        s = ''.join(words); cands += [s[:k] for k in range(lo, min(hi, len(s)) + 1)]
    if 'windows' in modes:
        for i in range(len(words)):
            acc = ''
            for w in words[i:]:
                acc += w
                if len(acc) > hi: break
                if len(acc) >= lo: cands.append(acc)
    for c in cands:
        if zlib.crc32(c.encode()) % N == shard and c not in seen:
            seen.add(c); out.write(c + '\n'); n += 1
print('tranche %d/%d : %d clés' % (shard, N, n), file=sys.stderr)
