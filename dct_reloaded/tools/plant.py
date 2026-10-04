"""Contrôle planté pour dct_solver.c : clair anglais réservé (Frankenstein) de n lettres, chiffré par double
transposition (mêmes conventions que mapping/encrypt2 de dct_solver.c) avec K1, K2 tirées d'un fichier de clés
(phrases), longueurs dans [wmin,wmax], premières entre elles. Usage :
python3 tools/plant.py cles.txt n graine sortie.txt [wmin=20] [wmax=27]  → écrit le chiffré, affiche K1, K2."""
import sys, random, math
keys_f, n, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
wmin = int(sys.argv[5]) if len(sys.argv) > 5 else 20; wmax = int(sys.argv[6]) if len(sys.argv) > 6 else 27
rnd = random.Random(seed)
keys = [l.strip() for l in open(keys_f) if wmin <= len(l.strip()) <= wmax]
k2 = rnd.choice(keys)
k1 = rnd.choice([k for k in keys[:200000] if len(k) != len(k2) and math.gcd(len(k), len(k2)) == 1])
txt = open('data/heldout/en_frankenstein.txt').read().strip()
o = rnd.randrange(len(txt) - n); P = [ord(c) - 97 for c in txt[o:o + n]]
def order(k):
    r = [sum(1 for j in range(len(k)) if k[j] < k[i] or (k[j] == k[i] and j < i)) for i in range(len(k))]
    o = [0] * len(k)
    for i, x in enumerate(r): o[x] = i
    return o
def mapping(n, w, perm):
    h, r = divmod(n, w); start = [0] * w; k = 0
    for j in range(w): col = perm[j]; start[col] = k; k += h + (col < r)
    return [start[i % w] + i // w for i in range(n)]
p1 = mapping(n, len(k1), order(k1)); p2 = mapping(n, len(k2), order(k2))
t = [0] * n
for i in range(n): t[p1[i]] = P[i]
c = [0] * n
for j in range(n): c[p2[j]] = t[j]
open(out, 'w').write(''.join(chr(97 + x) for x in c) + '\n')
print('K1=%s (%d) K2=%s (%d)' % (k1, len(k1), k2, len(k2)))
print('clair :', ''.join(chr(97 + x) for x in P[:60]))
