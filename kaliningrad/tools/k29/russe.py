"""K29 — suggestions 4 et 5 : apostrophes = signe mou ь ? mots russes translittérés (« gon'it' ») ? ê = э ?
1. Consonnes portant une apostrophe dans la bouteille, comparées aux consonnes suivies de ь en russe (liste de
   fréquence FrequencyWords ru_50k, pondérée par la fréquence) et au modèle « apostrophe posée au hasard sur une
   consonne de la bouteille » (log-vraisemblance multinomiale).
2. Mots de la bouteille trouvés dans un lexique russe translittéré (50 000 formes, 6 translittérations, ь = '),
   comparés aux « mots » de 500 bouteilles témoins : mêmes squelettes (longueurs, apostrophes, accents), lettres
   mélangées sur tout le texte. Même chose avec un lexique allemand (50 000 formes).
Usage : python3 tools/k29/russe.py <dossier contenant ru_50k.txt et de_50k.txt>"""
import sys, os, re, math, random, unicodedata
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'k18'))
from common import lines_v1
D = sys.argv[1]
rnd = random.Random(4)
L = lines_v1()[:25]
words = [w for l in L for w in l.split()]
def clean(w): return w.lower().replace('_', '').replace('.', '').replace('"', "'")
bw = [clean(w) for w in words if clean(w).replace("'", '')]
# --- 1. apostrophes
apo = Counter(); cons = Counter()
for w in bw:
    for i, c in enumerate(w):
        if c.isalpha() and c not in "aeiouêöü":
            cons[c] += 1
            if i + 1 < len(w) and w[i + 1] == "'": apo[c] += 1
CYR = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
C2L = {'б': 'b', 'в': 'w', 'г': 'g', 'д': 'd', 'ж': 'zh', 'з': 'z', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'п': 'p', 'р': 'r',
       'с': 's', 'т': 't', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch'}
ru = []
for line in open(os.path.join(D, 'ru_50k.txt'), encoding='utf-8'):
    w, n = line.split()
    if all(c in CYR for c in w): ru.append((w, int(n)))
soft = Counter()
for w, n in ru:
    for i in range(1, len(w)):
        if w[i] == 'ь' and w[i - 1] in C2L: soft[C2L[w[i - 1]]] += n
tot_soft = sum(soft.values())
print('== 1. consonnes portant une apostrophe (bouteille) et consonnes suivies de ь (russe, pondéré)')
print('%-5s %10s %12s %14s' % ('cons.', 'bouteille', 'russe ь %', 'consonnes bout. %'))
keys = sorted(set(apo) | {k for k, v in soft.items() if v / tot_soft > 0.01}, key=lambda k: -apo[k])
ncons = sum(cons.values())
for k in keys: print('%-5s %10d %12.1f %14.1f' % (k, apo[k], 100 * soft[k] / tot_soft, 100 * cons[k] / ncons))
def ll(dist, tot):
    return sum(o * math.log(max(dist.get(k, 0), 0.5) / tot) for k, o in apo.items())
ll_ru = ll(soft, tot_soft); ll_bt = ll(cons, ncons)
print('log-vraisemblance des %d apostrophes : modèle ь russe %.1f ; apostrophe au hasard sur une consonne de la bouteille %.1f'
      % (sum(apo.values()), ll_ru, ll_bt))
nb_letters = sum(1 for w in bw for c in w if c.isalpha())
ru_letters = sum(n * len(w) for w, n in ru); ru_soft = sum(n * w.count('ь') for w, n in ru)
print('taux : bouteille %.1f %% des lettres portent une apostrophe ; ь = %.1f %% des lettres russes'
      % (100 * sum(apo.values()) / nb_letters, 100 * ru_soft / ru_letters))
# --- 2. lexiques
def translits():
    base = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': "'", 'э': 'e', 'ю': 'ju', 'я': 'ja'}
    out = []
    for var in range(6):
        t = dict(base)
        if var in (1, 4): t.update({'в': 'w', 'ж': 'sh', 'ш': 'sch', 'ч': 'tsch', 'ц': 'z', 'х': 'ch', 'э': 'ê'})   # à l'allemande
        if var in (2, 5): t.update({'й': 'i', 'ы': 'i', 'ю': 'iu', 'я': 'ia', 'х': 'h', 'э': 'ê', 'ц': 'c', 'ш': 's', 'ч': 'c', 'ж': 'z'})  # sans j/y
        if var == 3: t.update({'х': 'h', 'ц': 'c', 'ч': 'c', 'ш': 's', 'щ': 's', 'ж': 'z', 'й': 'j', 'ю': 'yu', 'я': 'ya'})
        if var >= 4: t.update({'ь': ''})
        out.append(t)
    return out
lex_ru = set()
for t in translits():
    for w, n in ru: lex_ru.add(''.join(t[c] for c in w))
lex_de = set()
for line in open(os.path.join(D, 'de_50k.txt'), encoding='utf-8'):
    w = line.split()[0].lower()
    if w.isalpha(): lex_de.add(w.replace('ä', 'ê'))
def norm_variants(w):
    a = w; b = w.replace("'", ''); c = unicodedata.normalize('NFKD', b).encode('ascii', 'ignore').decode()
    return {a, b, c, a.replace('ê', 'e')}
def hits(ws, lex, minlen):
    return [w for w in ws if len(w.replace("'", '')) >= minlen and norm_variants(w) & lex]
# témoins : squelettes conservés, lettres mélangées
letters = [c for w in bw for c in w if c.isalpha()]
def fake():
    sh = letters[:]; rnd.shuffle(sh); it = iter(sh); out = []
    for w in bw:
        out.append(''.join(next(it) if c.isalpha() else c for c in w))
    return out
print('\n== 2. mots de la bouteille présents dans un lexique (%d formes russes translittérées, %d allemandes)' % (len(lex_ru), len(lex_de)))
for name, lex in (('russe', lex_ru), ('allemand', lex_de)):
    for minlen in (2, 3, 4, 5):
        h = hits(bw, lex, minlen)
        ctrl = [len(hits(fake(), lex, minlen)) for _ in range(500)]
        m = sum(ctrl) / len(ctrl); sd = (sum((x - m) ** 2 for x in ctrl) / len(ctrl)) ** .5
        p = sum(x >= len(h) for x in ctrl) / len(ctrl)
        print('%-9s longueur >= %d : bouteille %3d (%s) | témoins %.1f ± %.1f | p = %.3f'
              % (name, minlen, len(h), ' '.join(sorted(set(h), key=len, reverse=True)[:12]), m, sd, p))
o_rate = sum(n * w.count('о') for w, n in ru) / ru_letters
print('\no en russe : %.1f %% des lettres ; dans la bouteille : %.1f %%' % (100 * o_rate, 100 * sum(c == 'o' for c in letters) / len(letters)))
e_rev = sum(n * w.count('э') for w, n in ru) / ru_letters
print('э en russe : %.2f %% (%.1f par 979 lettres) ; ê dans la bouteille : %d' % (100 * e_rev, 979 * e_rev, sum(c == 'ê' for c in letters)))
