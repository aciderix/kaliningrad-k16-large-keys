"""K29 — contrôles pour affine.c : allemand réservé + nuls f/w/n, blocs S1–S5 chiffrés par une même marche affine
13×13 (La Loubère par défaut, départ et sens tirés au hasard, ou une marche quelconque), S6 par une marche 12×12.
Usage : python3 tools/k29/affine_ctrl.py graine sortie.txt [nuls=0.10] [loubere|quelconque]"""
import sys, random, re
seed, out = int(sys.argv[1]), sys.argv[2]
nul = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
kind = sys.argv[4] if len(sys.argv) > 4 else 'loubere'
rnd = random.Random(seed)
BL = [166, 169, 162, 169, 169, 144]
txt = re.sub('[^a-z]', '', open('data/heldout/de.txt').read().lower())
o = rnd.randrange(2000, len(txt) - 1200); P = []; i = o
while len(P) < 979:
    if rnd.random() < nul: P.append(rnd.choices('fwn', weights=[32, 19, 48])[0])
    else: P.append(txt[i]); i += 1
def build(n, a, b, c, d, r0, c0, dr, ln):
    N = n * n; cell = [(((r0 + a * (k % n) + b * (k // n)) % n) * n + ((c0 + c * (k % n) + d * (k // n)) % n)) for k in range(N)]
    src = [0] * ln
    if dr == 0:
        valid = set(cell[k] for k in range(ln)); rank = {}; j = 0
        for x in range(N):
            if x in valid: rank[x] = j; j += 1
        for k in range(ln): src[k] = rank[cell[k]]
    else:
        j = 0
        for k in range(N):
            x = cell[k]
            if x < ln: src[x] = j; j += 1
    return src
def rkey(n):
    while True:
        a, b, c, d = (rnd.randrange(n) for _ in range(4)); det = (a * d - b * c) % n
        if (n == 13 and det) or (n == 12 and det % 2 and det % 3): return a, b, c, d
k13 = (12, 2, 1, 12) if kind == 'loubere' else rkey(13)
r0, c0, dr = rnd.randrange(13), rnd.randrange(13), rnd.randrange(2)
k12 = rkey(12); r1, c1, d1 = rnd.randrange(12), rnd.randrange(12), rnd.randrange(2)
C = []; off = 0
for b, ln in enumerate(BL):
    src = build(13, *k13, r0, c0, dr, ln) if b < 5 else build(12, *k12, r1, c1, d1, ln)
    blk = [None] * ln
    for k in range(ln): blk[src[k]] = P[off + k]
    C += blk; off += ln
open(out, 'w').write(''.join(C) + '\n')
print('clé 13x13 [[%d,%d],[%d,%d]] départ (%d,%d) sens %d ; clé 12x12 [[%d,%d],[%d,%d]] départ (%d,%d) sens %d'
      % (*k13, r0, c0, dr, *k12, r1, c1, d1))
print('clair :', ''.join(P[:60]))
