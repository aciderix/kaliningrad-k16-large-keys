"""K28 complément — les signes de l'habillage marquent-ils des lettres nulles ?
Si l'auteur avait inséré des nuls dans un texte laissé dans l'ordre en les signalant (apostrophe, accent, abréviation),
les retirer rendrait les liens entre voisines. On retire chaque catégorie de lettres marquées, puis on mesure
l'information mutuelle entre voisines (z contre 400 mélanges) et la note de quadrigrammes allemands.
Usage : python3 tools/k28/marques.py"""
import sys, re, random, math, numpy as np
from collections import Counter
sys.path.insert(0, 'tools/k18')
from common import lines_v1, mi
import unicodedata
QG = np.fromfile('data/models/qg_de.bin', dtype='<f4')
def score(s):
    a = np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64) - 97
    return float(QG[((a[:-3] * 26 + a[1:-2]) * 26 + a[2:-1]) * 26 + a[3:]].mean())
L = lines_v1()[:25]
toks = []   # (lettre, apostrophe, accent, abréviation, soulignée)
for line in L:
    for w in line.split():
        abbr = bool(re.fullmatch(r"([a-zêöü]\.)+", w.lower().replace("'", '').replace('_', '')))
        i = 0
        while i < len(w):
            ch = w[i]
            if ch.isalpha():
                apo = i + 1 < len(w) and w[i + 1] in "'\""
                und = i + 1 < len(w) and w[i + 1] == '_'
                base = unicodedata.normalize('NFKD', ch.lower()).encode('ascii', 'ignore').decode()
                toks.append((base, apo, ch.lower() in 'êöü', abbr, und))
            i += 1
assert len(toks) == 979, len(toks)
cats = {'rien': lambda t: False, 'lettres apostrophées': lambda t: t[1], "n' seulement": lambda t: t[1] and t[0] == 'n',
        'lettres accentuées': lambda t: t[2], 'abréviations': lambda t: t[3], 'apostrophées + accentuées': lambda t: t[1] or t[2]}
rnd = random.Random(5)
print('%-28s %6s %8s %8s %8s' % ('retirées', 'reste', 'MI z', 'quadri', 'témoins'))
for name, f in cats.items():
    s = ''.join(t[0] for t in toks if not f(t))
    m0 = mi(list(s)); ms = []; qs = []
    for _ in range(400):
        x = list(s); rnd.shuffle(x); ms.append(mi(x)); qs.append(score(''.join(x)))
    print('%-28s %6d %+8.2f %8.3f %8.3f' % (name, len(s), (m0 - np.mean(ms)) / np.std(ms), score(s), np.mean(qs)))
