"""Vérifier une « solution » proposée pour la bouteille (K28).
Donne, pour un clair proposé (fichier texte, n'importe quelle orthographe ; ä→a, ß→ss, etc.) :
 1. le bilan des lettres : ce que la bouteille a en trop (nuls nécessaires) ou en moins (impossible sans erreur de
    lecture) — une transposition pure exige un bilan nul ;
 2. le déplacement maximal D nécessaire pour passer du clair à la bouteille si chaque lettre n'a bougé que localement
    (appariement lettre à lettre dans l'ordre, positions mises à l'échelle) ;
 3. la même mesure sur 200 fenêtres d'allemand sans rapport de même longueur : une vraie solution doit faire nettement
    mieux que des textes quelconques, sinon la proposition n'est qu'un texte compatible parmi d'autres (K22).
Usage : python3 tools/k28/verifier.py proposition.txt [corpus_allemand.txt=data/heldout/de.txt]"""
import sys, re, unicodedata, random
from collections import Counter, defaultdict
def norm(s):
    s = s.lower().replace('ß', 'ss')
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub('[^a-z]', '', s)
B = norm(open('data/ciphertext_979.txt').read())
P = norm(open(sys.argv[1], encoding='utf-8').read())
ref = norm(open(sys.argv[2] if len(sys.argv) > 2 else 'data/heldout/de.txt', encoding='utf-8', errors='ignore').read())
def balance(p):
    cb, cp = Counter(B), Counter(p)
    extra = {c: cb[c] - cp[c] for c in sorted(set(cb) | set(cp)) if cb[c] > cp[c]}
    miss = {c: cp[c] - cb[c] for c in sorted(set(cb) | set(cp)) if cp[c] > cb[c]}
    return extra, miss
def feasible(p, D):
    """chaque lettre du clair (position mise à l'échelle) trouve une lettre identique de la bouteille à moins de D"""
    pos = defaultdict(list)
    for j, c in enumerate(B): pos[c].append(j)
    used = {c: 0 for c in pos}; k = len(B) / len(p)
    occ = defaultdict(list)
    for i, c in enumerate(p): occ[c].append(i * k)
    for c, xs in occ.items():
        bs = pos.get(c, []); t = 0
        for x in xs:                       # glouton de gauche à droite : optimal pour des intervalles sur une droite
            while t < len(bs) and bs[t] < x - D: t += 1
            if t == len(bs) or bs[t] > x + D: return False
            t += 1
    return True
def minD(p):
    lo, hi = 0, len(B)
    if not feasible(p, hi): return None
    while lo < hi:
        m = (lo + hi) // 2
        if feasible(p, m): hi = m
        else: lo = m + 1
    return lo
extra, miss = balance(P)
print('clair proposé : %d lettres ; bouteille : %d' % (len(P), len(B)))
print('lettres de la bouteille absentes du clair (nuls nécessaires, %d) : %s' % (sum(extra.values()), extra))
print('lettres du clair absentes de la bouteille (%d) : %s' % (sum(miss.values()), miss))
if miss:
    print('=> incompatible avec toute transposition, même avec des nuls, sauf erreurs de lecture.')
    sys.exit()
d = minD(P)
rnd = random.Random(1); ds = []
for _ in range(200):
    o = rnd.randrange(0, len(ref) - len(P)); w = ref[o:o + len(P)]
    if not balance(w)[1]: ds.append(minD(w))
print('déplacement maximal nécessaire D = %s' % d)
if ds:
    ds.sort(); r = sum(x <= d for x in ds) / len(ds)
    print('fenêtres allemandes sans rapport compatibles : %d/200 ; leur D : min %d, médiane %d ; part avec D <= proposé : %.2f'
          % (len(ds), ds[0], ds[len(ds) // 2], r))
else:
    print('aucune fenêtre allemande de cette longueur ne tient dans les lettres de la bouteille (la proposition est donc déjà remarquable)')
