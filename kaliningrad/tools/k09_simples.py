#!/usr/bin/env python3
"""K09 — barrière (rail fence) et décimation, recherche exhaustive (voir experiments/K09_transpositions_simples/).
Usage : python3 tools/k09_simples.py [controles|reel] [nnull]"""
import sys, os, random, math
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import k06_routes as k6
import k07_routes_mi as k7
R = random.Random(909); NR = np.random.default_rng(909)

def catalogue(n):
    names, perms = [], []
    for r in range(2, min(100, n // 2) + 1):
        L = 2 * r - 2
        for o in range(L):
            rail = [(t if t < r else L - t) for t in ((i + o) % L for i in range(n))]
            p = np.array(sorted(range(n), key=lambda i: (rail[i], i)), dtype=np.int64)   # C[j] = P[p[j]]
            inv = np.empty_like(p); inv[p] = np.arange(n)
            names += [('barriere', r, o, 'dechiffre'), ('barriere', r, o, 'chiffre')]; perms += [inv, p]
    for k in range(2, n):
        if math.gcd(k, n) == 1:
            names.append(('decimation', k, 0, '')); perms.append((np.arange(n) * k) % n)
    return names, np.array(perms)

def best_q(c, perms):
    b, a = k6.scores(c, perms); return b, a

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    heb = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', 'de.txt')).read()
    de = np.array([ord(ch) - 65 for ch in heb if 'A' <= ch <= 'Z'], dtype=np.int64)
    if mode == 'controles':
        for n in (169, 979):
            names, perms = catalogue(n)
            for fam in ('barriere', 'decimation'):
                idx = [i for i, x in enumerate(names) if x[0] == fam]
                okq = okm = 0
                for t in range(10):
                    o = R.randrange(len(de) - n); P = de[o:o + n]; j = R.choice(idx)
                    C = np.empty(n, dtype=np.int64); C[perms[j]] = P                  # P = C[perm_j]
                    b, a = best_q(C, perms); i = int(np.argmax(b))
                    invj = np.empty(n, dtype=np.int64); invj[perms[j]] = np.arange(n)
                    def ok(pi):   # critère (amendement 1) : >= 90 % des voisines recollées (sens et rotation indifférents)
                        q = invj[perms[pi]]; d = np.abs(np.diff(q)); return (np.minimum(d, n - d) == 1).mean() >= 0.9
                    okq += ok(i)
                    sub = np.array(R.sample(range(26), 26)); Cs = sub[C]
                    m = k7.best_mi(Cs, perms); i2 = int(np.argmax(m)); cs = Cs[perms[i2]]
                    okm += ok(i2)
                print(f"n={n} {fam}: quadrigrammes {okq}/10 ; MI (sous substitution) {okm}/10 ; catalogue {len(perms)}", flush=True)
    else:
        nnull = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        for name, c in k6.load_seqs().items():
            c = c.astype(np.int64); n = len(c); names, perms = catalogue(n)
            b, a = best_q(c, perms); i = int(np.argmax(b))
            nq = [best_q(NR.permutation(c), perms)[0].max() for _ in range(nnull)]
            txt = ''.join(chr(97 + x) for x in (c[perms[i]][::-1] if a[i] else c[perms[i]]))
            line = (f"{name} (n={n}) : quadri max {b[i]:.4f} {names[i]} | nuls max {max(nq):.4f} moy {np.mean(nq):.4f} | "
                    f"p={(sum(x >= b[i] for x in nq) + 1) / (nnull + 1):.3f}")
            if name == 'tout':
                m = k7.best_mi(c, perms); j = int(np.argmax(m))
                nm = [k7.best_mi(NR.permutation(c), perms).max() for _ in range(nnull)]
                line += (f"\n    MI max {m[j]:.4f} {names[j]} | nuls max {max(nm):.4f} moy {np.mean(nm):.4f} | "
                         f"p={(sum(x >= m[j] for x in nm) + 1) / (nnull + 1):.3f}")
            print(line + f"\n    {txt[:150]}", flush=True)
