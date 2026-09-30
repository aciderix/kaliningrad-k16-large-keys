#!/usr/bin/env python3
"""K07, famille 1 — catalogue de routes (K06) noté par MI(1), invariant par substitution.
Usage : python3 tools/k07_routes_mi.py [controles|reel] [nnull]"""
import sys, os, random
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import k06_routes as k6
R = random.Random(707); NR = np.random.default_rng(707)

def mi_rows(P):
    """MI(1) de chaque ligne de P (M × n, lettres 0..25)."""
    M, n = P.shape
    codes = (P[:, :-1] * 26 + P[:, 1:]) + (np.arange(M)[:, None] * 676)
    cnt = np.bincount(codes.ravel(), minlength=M * 676).reshape(M, 26, 26).astype(float)
    p = cnt / (n - 1); px = p.sum(2, keepdims=True); py = p.sum(1, keepdims=True)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(p > 0, p * np.log2(p / (px * py)), 0.0)
    return t.sum((1, 2))

def best_mi(c, perms):
    best = np.empty(len(perms))
    for s in range(0, len(perms), 2000):
        best[s:s + 2000] = mi_rows(c[perms[s:s + 2000]])
    return best

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    if mode == 'controles':
        heb = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', 'de.txt')).read()
        de = np.array([ord(ch) - 65 for ch in heb if 'A' <= ch <= 'Z'], dtype=np.int64)
        for n in (169, 144, 979):
            names, perms = k6.catalogue(n); ok = 0
            for t in range(10):
                o = R.randrange(len(de) - n); sub = np.array(R.sample(range(26), 26))
                P = sub[de[o:o + n]]; j = R.randrange(len(perms))
                C = np.empty(n, dtype=np.int64); C[perms[j]] = P
                b = best_mi(C, perms); i = int(np.argmax(b))
                good = C[perms[i]].tolist() == P.tolist() or C[perms[i]][::-1].tolist() == P.tolist()
                ok += good
                print(f"  n={n} essai {t}: vrai {names[j]} | trouvé {names[i]} MI={b[i]:.3f} (vrai {b[j]:.3f}) {'OK' if good else 'ÉCHEC'}")
            print(f"n={n} : {ok}/10", flush=True)
    else:
        nnull = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        for name, c in k6.load_seqs().items():
            c = c.astype(np.int64); n = len(c); names, perms = k6.catalogue(n)
            b = best_mi(c, perms); i = int(np.argmax(b))
            nulls = [best_mi(NR.permutation(c), perms).max() for _ in range(nnull)]
            p = (sum(x >= b[i] for x in nulls) + 1) / (nnull + 1)
            txt = ''.join(chr(97 + x) for x in c[perms[i]])
            print(f"{name} (n={n}) : MI max {b[i]:.4f} {names[i]} | nuls max {max(nulls):.4f} moyenne {np.mean(nulls):.4f} | p={p:.3f}\n    {txt[:160]}", flush=True)
