#!/usr/bin/env python3
"""K06 — routes classiques, recherche exhaustive (voir experiments/K06_routes/PREREGISTRATION.md).
Usage : python3 tools/k06_routes.py [controles|reel] [nnull]"""
import sys, os, random
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
QG = np.fromfile(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'models', 'qg_de.bin'), dtype='<f4')
R = random.Random(606); NR = np.random.default_rng(606)

def routes(n, w):
    h = (n + w - 1) // w
    ok = lambda r, c: 0 <= r < h and 0 <= c < w and r * w + c < n
    out = {}
    def add(name, cells):
        seq = [r * w + c for r, c in cells if ok(r, c)]
        if len(seq) == n: out[name] = seq
    for lr in (0, 1):
        cols = range(w) if lr == 0 else range(w - 1, -1, -1)
        for ud in (0, 1):
            add(f'col{lr}{ud}', [(r, c) for c in cols for r in (range(h) if ud == 0 else range(h - 1, -1, -1))])
            add(f'colzz{lr}{ud}', [(r, c) for i, c in enumerate(cols) for r in (range(h) if (i + ud) % 2 == 0 else range(h - 1, -1, -1))])
    for tb in (0, 1):
        rows = range(h) if tb == 0 else range(h - 1, -1, -1)
        for lr in (0, 1):
            add(f'rowzz{tb}{lr}', [(r, c) for i, r in enumerate(rows) for c in (range(w) if (i + lr) % 2 == 0 else range(w - 1, -1, -1))])
    for fam in ('anti', 'main'):
        ks = range(h + w - 1) if fam == 'anti' else range(-(h - 1), w)
        for kd in (0, 1):
            for rd in (0, 1):
                cells = []
                for k in (ks if kd == 0 else reversed(ks)):
                    rr = range(h) if rd == 0 else range(h - 1, -1, -1)
                    cells += [(r, k - r) if fam == 'anti' else (r, k + r) for r in rr]
                add(f'diag{fam}{kd}{rd}', cells)
    for corner in range(4):
        for cw in (0, 1):
            top, bot, lef, rig = 0, h - 1, 0, w - 1; cells = []
            # spirale sur le rectangle complet, départ au coin donné ; les cases hors texte sont sautées par add()
            seqs = []
            while top <= bot and lef <= rig:
                ring = [(top, c) for c in range(lef, rig + 1)] + [(r, rig) for r in range(top + 1, bot + 1)]
                if top < bot: ring += [(bot, c) for c in range(rig - 1, lef - 1, -1)]
                if lef < rig: ring += [(r, lef) for r in range(bot - 1, top, -1)]
                seqs.append(ring); top += 1; bot -= 1; lef += 1; rig -= 1
            for ring in seqs:
                # anneau horaire depuis le coin haut-gauche ; on le fait tourner/miroir selon coin et sens
                if cw == 0: ring = [ring[0]] + ring[:0:-1]
                if ring:
                    tgt = [(min(p[0] for p in ring), min(p[1] for p in ring)), (min(p[0] for p in ring), max(p[1] for p in ring)),
                           (max(p[0] for p in ring), max(p[1] for p in ring)), (max(p[0] for p in ring), min(p[1] for p in ring))][corner]
                    i = ring.index(tgt) if tgt in ring else 0
                    ring = ring[i:] + ring[:i]
                cells += ring
            add(f'spir{corner}{cw}', cells)
    return out

def catalogue(n):
    names, perms = [], []
    for w in range(2, n // 2 + 1):
        for name, p in routes(n, w).items():
            p = np.array(p, dtype=np.int32); inv = np.empty_like(p); inv[p] = np.arange(n)
            names += [(w, name, 'lire'), (w, name, 'inverse')]; perms += [p, inv]
    return names, np.array(perms)

def scores(c, perms):
    best = np.full(len(perms), -1e9); arg = np.zeros(len(perms), dtype=int)
    for s in range(0, len(perms), 3000):
        P = c[perms[s:s + 3000]].astype(np.int32)
        for rev in (0, 1):
            X = P[:, ::-1] if rev else P
            v = QG[((X[:, :-3] * 26 + X[:, 1:-2]) * 26 + X[:, 2:-1]) * 26 + X[:, 3:]].mean(1)
            m = v > best[s:s + 3000]; best[s:s + 3000][m] = v[m]; arg[s:s + 3000][m] = rev
    return best, arg

def load_seqs():
    import k02_contacts as k
    secs, _ = k.load_real()
    seqs = {f'S{i + 1}': np.array(s, dtype=np.int32) for i, s in enumerate(secs)}
    seqs['tout'] = np.concatenate([seqs[f'S{i + 1}'] for i in range(6)])
    return seqs

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    heb = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', 'de.txt')).read()
    de = np.array([ord(ch) - 65 for ch in heb if 'A' <= ch <= 'Z'], dtype=np.int32)
    if mode == 'controles':
        for n in (169, 144, 984):
            names, perms = catalogue(n); ok = 0
            for t in range(10):
                o = R.randrange(len(de) - n); P = de[o:o + n]; j = R.randrange(len(perms)); rev = R.randrange(2)
                Pc = P[::-1] if rev else P; C = np.empty(n, dtype=np.int32); C[perms[j]] = Pc   # P_cand = C[perm]
                b, a = scores(C, perms); i = int(np.argmax(b))
                good = (C[perms[i]][::-1] if a[i] else C[perms[i]]).tolist() == P.tolist()
                ok += good
                print(f"  n={n} essai {t}: vrai {names[j]} rev={rev} | trouvé {names[i]} rev={a[i]} score={b[i]:.3f} {'OK' if good else 'ÉCHEC'}")
            print(f"n={n} : {ok}/10 retrouvés ; catalogue = {len(perms)} lectures (×2 sens)")
    else:
        nnull = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        for name, c in load_seqs().items():
            n = len(c); names, perms = catalogue(n)
            b, a = scores(c, perms); i = int(np.argmax(b))
            nulls = []
            for _ in range(nnull):
                bb, _ = scores(NR.permutation(c), perms); nulls.append(bb.max())
            txt = ''.join(chr(97 + x) for x in (c[perms[i]][::-1] if a[i] else c[perms[i]]))
            p = (sum(x >= b[i] for x in nulls) + 1) / (nnull + 1)
            print(f"{name} (n={n}, {len(perms)} lectures) : meilleur {b[i]:.4f} {names[i]} rev={a[i]} | nuls max {max(nulls):.4f} "
                  f"moyenne {np.mean(nulls):.4f} | p={p:.3f}\n    {txt[:200]}", flush=True)
