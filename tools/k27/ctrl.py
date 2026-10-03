"""K27 — contrôle planté : allemand réservé (Kafka, data/heldout/de.txt) + ~10 % de nuls f/w/n à des places tirées
au hasard (proportions des excès de la bouteille 32:19:48), chiffré par double transposition avec deux clés tirées
d'un fichier de clés. Usage : python3 tools/k27/ctrl.py cles.txt graine sortie.txt [mode whole|blocks] [nuls=99] [variantes : base|toutes]
Écrit le chiffré (979 lettres) ; affiche les clés et la variante utilisées."""
import sys, random, re
keys = [l.rstrip('\n').split('\t') for l in open(sys.argv[1], encoding='utf-8')]
seed = int(sys.argv[2]); out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else 'whole'
nnul = int(sys.argv[5]) if len(sys.argv) > 5 else 99
allv = len(sys.argv) > 6 and sys.argv[6] == 'toutes'
rnd = random.Random(seed)
txt = re.sub('[^a-z]', '', open('data/heldout/de.txt').read().lower())
L = 979; m = L - nnul; o = rnd.randrange(2000, len(txt) - m - 1); P = list(txt[o:o + m])
for _ in range(nnul):
    P.insert(rnd.randrange(len(P) + 1), rnd.choices('fwn', weights=[32, 19, 48])[0])
def perm(r, inv, L):
    n = len(r); order = [0] * n
    for c in range(n):
        if inv: order[c] = r[c]
        else: order[r[c]] = c
    return [i for t in range(n) for i in range(order[t], L, n)]
a, b = rnd.choice(keys), rnd.choice(keys); va, vb = rnd.randrange(4 if allv else 2), rnd.randrange(4 if allv else 2)
ra = list(map(int, a[1].split()[1:])); rb = list(map(int, b[1].split()[1:]))
def step(P, r, v):
    e = perm(r, v & 1, len(P))
    if v & 2:                       # sens inverse : écrire dans les colonnes (ordre de la clé), lire en lignes
        Q = [None] * len(P)
        for j, i in enumerate(e): Q[i] = P[j]
        return Q
    return [P[i] for i in e]
def dt(P): return step(step(P, ra, va), rb, vb)
if mode == 'whole': C = dt(P)
else:
    C = []; o = 0
    for bl in (166, 169, 162, 169, 169, 144): C += dt(P[o:o + bl]); o += bl
open(out, 'w').write(''.join(C) + '\n')
print('clair  :', ''.join(P[:100]))
print('clés   : A=%s B=%s v=%d%d' % (a[0], b[0], va, vb))
