#!/usr/bin/env python3
"""K15, famille R — même route (catalogue K06 : route, largeur, lecture/inverse, sens) pour les 6 blocs ; scores additionnés.
Usage : python3 tools/k15_routes.py [controles|reel] [nnull]"""
import sys, os, random
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import k06_routes as k6
QG = k6.QG
R = random.Random(1515); NR = np.random.default_rng(1515)
SIZES = [166, 169, 162, 169, 169, 144]

def common_catalogue(sizes):
    cats = []
    for n in sizes:
        names, perms = k6.catalogue(n); cats.append(dict(zip(names, perms)))
    keys = [k for k in cats[0] if all(k in c for c in cats[1:])]
    return keys, [[c[k] for k in keys] for c in cats]

def pooled_scores(blocks, keys, perms_by_block):
    """renvoie (MI additionné, meilleur quadrigramme moyen sur les 2 sens) pour chaque entrée commune"""
    M = len(keys); cnt = np.zeros((M, 676)); qsum = np.zeros((M, 2)); qn = 0
    for c, perms in zip(blocks, perms_by_block):
        P = c[np.array(perms)]                       # M × n
        codes = P[:, :-1] * 26 + P[:, 1:]
        for m in range(M): cnt[m] += np.bincount(codes[m], minlength=676)
        for rev in (0, 1):
            X = P[:, ::-1] if rev else P
            qsum[:, rev] += QG[((X[:, :-3] * 26 + X[:, 1:-2]) * 26 + X[:, 2:-1]) * 26 + X[:, 3:]].sum(1)
        qn += P.shape[1] - 3
    p = cnt / cnt.sum(1, keepdims=True); px = p.reshape(M, 26, 26).sum(2); py = p.reshape(M, 26, 26).sum(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(p.reshape(M, 26, 26) > 0, p.reshape(M, 26, 26) * np.log2(p.reshape(M, 26, 26) / (px[:, :, None] * py[:, None, :])), 0)
    return t.sum((1, 2)), qsum.max(1) / qn

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    keys, pbb = common_catalogue(SIZES)
    print(f"entrées communes du catalogue : {len(keys)}", flush=True)
    if mode == 'controles':
        heb = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', 'de.txt')).read()
        de = np.array([ord(ch) - 65 for ch in heb if 'A' <= ch <= 'Z'], dtype=np.int64)
        for score in ('MI', 'Q'):
            ok = 0
            for t in range(10):
                o = R.randrange(len(de) - 1100); j = R.randrange(len(keys)); sub = np.array(R.sample(range(26), 26)) if score == 'MI' else np.arange(26)
                blocks = []; k = o
                for b, n in enumerate(SIZES):
                    P = sub[de[k:k + n]]; k += n; C = np.empty(n, dtype=np.int64); C[pbb[b][j]] = P; blocks.append(C)
                mi, q = pooled_scores(blocks, keys, pbb); i = int(np.argmax(mi if score == 'MI' else q))
                good = tot = 0
                for b, n in enumerate(SIZES):
                    inv = np.empty(n, dtype=np.int64); inv[pbb[b][j]] = np.arange(n); qq = inv[pbb[b][i]]
                    good += (np.abs(np.diff(qq)) == 1).sum(); tot += n - 1
                ok += good >= 0.9 * tot
                print(f"  {score} essai {t}: vrai {keys[j]} | trouvé {keys[i]} contacts {good}/{tot}", flush=True)
            print(f"==> {score} : {ok}/10", flush=True)
    else:
        import k02_contacts as k2
        secs, _ = k2.load_real(); blocks = [np.array(s, dtype=np.int64) for s in secs]
        nnull = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        mi, q = pooled_scores(blocks, keys, pbb)
        nm, nq = [], []
        for _ in range(nnull):
            a, b = pooled_scores([NR.permutation(x) for x in blocks], keys, pbb); nm.append(a.max()); nq.append(b.max())
        im, iq = int(np.argmax(mi)), int(np.argmax(q))
        print(f"MI additionné : réel {mi[im]:.4f} {keys[im]} | nuls max {max(nm):.4f} moy {np.mean(nm):.4f} | p={(sum(x >= mi[im] for x in nm) + 1) / (nnull + 1):.3f}")
        print(f"quadrigrammes : réel {q[iq]:.4f} {keys[iq]} | nuls max {max(nq):.4f} moy {np.mean(nq):.4f} | p={(sum(x >= q[iq] for x in nq) + 1) / (nnull + 1):.3f}")
