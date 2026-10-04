#!/usr/bin/env python3
"""K12 — empreinte du flux contre des familles de chiffres synthétiques (voir experiments/K12_empreinte_du_flux/).
Usage : python3 tools/k12_empreinte.py [controles|reel]"""
import sys, os, random, collections
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
R = random.Random(1212); NR = np.random.default_rng(1212)
N = 979; A25 = [c for c in range(26) if c != 9]   # sans j

def load(lang):
    t = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', f'{lang}.txt')).read()
    return np.array([ord(c) - 65 for c in t if 'A' <= c <= 'Z'])

# ---------- statistiques ----------
def ic(x): c = np.bincount(x, minlength=26); n = len(x); return float((c * (c - 1)).sum() / (n * (n - 1)))
def mi(x, d):
    c = np.bincount(x[:-d] * 26 + x[d:], minlength=676).reshape(26, 26).astype(float); p = c / c.sum()
    px = p.sum(1, keepdims=True); py = p.sum(0, keepdims=True); m = p > 0
    return float((p[m] * np.log2(p[m] / (px @ py)[m])).sum())
def rep3(x):
    c = collections.Counter(zip(x[:-2], x[1:-1], x[2:])); return sum(v for v in c.values() if v > 1)
def stats(x, nsh=20):
    sh = [NR.permutation(x) for _ in range(nsh)]
    e2 = mi(x, 1) - np.mean([mi(s, 1) for s in sh]); e3 = mi(x, 2) - np.mean([mi(s, 2) for s in sh])
    e4 = max(np.mean([ic(x[j::p]) for j in range(p)]) for p in range(2, 21))
    ev, od = np.bincount(x[0::2], minlength=26), np.bincount(x[1::2], minlength=26); tot = ev + od; m = tot > 0
    e5 = float((((ev - tot * len(x[0::2]) / len(x)) ** 2) / np.maximum(tot * len(x[0::2]) / len(x), 1e-9))[m].sum()
               + (((od - tot * len(x[1::2]) / len(x)) ** 2) / np.maximum(tot * len(x[1::2]) / len(x), 1e-9))[m].sum())
    e6 = int(np.sum(x[0:-1:2] == x[1::2]))
    e7 = int(len(set(x.tolist())))
    e8 = rep3(x) - np.mean([rep3(s) for s in sh[:5]])
    return np.array([ic(x), e2, e3, e4, e5, e6, e7, e8])
NAMES = ['IC', 'MI1', 'MI2', 'ICperiod', 'pair/impair', 'doublets(2k)', 'nb lettres', 'trigr.rép']

# ---------- familles ----------
def sub(x): p = np.array(R.sample(range(26), 26)); return p[x]
def vig(x): k = np.array([R.randrange(26) for _ in range(R.randint(3, 12))]); return (x + np.resize(k, len(x))) % 26
def colt(x):
    w = R.randint(5, 20); key = list(range(w)); R.shuffle(key)
    return np.concatenate([x[c::w] for c in key])
def playfair(x):
    sq = A25[:]; R.shuffle(sq); pos = {c: (i // 5, i % 5) for i, c in enumerate(sq)}
    t = [9 - 1 if c == 9 else c for c in x]   # j -> i
    pairs = []; i = 0
    while i < len(t):
        a = t[i]; b = t[i + 1] if i + 1 < len(t) else 23
        if a == b: b = 23 if a != 23 else 16; i += 1
        else: i += 2
        pairs.append((a, b))
    out = []
    for a, b in pairs:
        (ra, ca), (rb, cb) = pos[a], pos[b]
        if ra == rb: out += [sq[ra * 5 + (ca + 1) % 5], sq[rb * 5 + (cb + 1) % 5]]
        elif ca == cb: out += [sq[((ra + 1) % 5) * 5 + ca], sq[((rb + 1) % 5) * 5 + cb]]
        else: out += [sq[ra * 5 + cb], sq[rb * 5 + ca]]
    return np.array(out[:len(x)])
def bifid(x):
    sq = A25[:]; R.shuffle(sq); pos = {c: (i // 5, i % 5) for i, c in enumerate(sq)}; P = R.randint(5, 10)
    t = [8 if c == 9 else c for c in x]; out = []
    for s in range(0, len(t), P):
        blk = t[s:s + P]; rows = [pos[c][0] for c in blk]; cols = [pos[c][1] for c in blk]; z = rows + cols
        out += [sq[z[2 * i] * 5 + z[2 * i + 1]] for i in range(len(blk))]
    return np.array(out)
FREQ_DE = None
def homoph(x):
    f = np.bincount(x, minlength=26).astype(float); order = np.argsort(-f)
    # 26 symboles : les lettres fréquentes reçoivent plusieurs symboles, les plus rares partagent (fusion)
    counts = np.zeros(26, int); counts[order[:14]] = 1
    extra = 26 - 14; share = f[order[:14]] / f[order[:14]].sum()
    for i in np.argsort(-share)[:extra]: counts[order[i]] += 1
    syms = list(range(26)); R.shuffle(syms); table = {}; k = 0
    for L in order[:14]:
        table[L] = syms[k:k + counts[L]]; k += counts[L]
    for L in order[14:]: table[L] = [R.choice(syms)]
    return np.array([R.choice(table[c]) for c in x])
def iid(freq): return lambda x: NR.choice(26, size=len(x), p=freq)

FAMS = ['F1 clair', 'F2 substitution', 'F3 Vigenère', 'F4 transposition', 'F5 subst+transp', 'F6 Playfair', 'F7 Bifid',
        'F8 homophonique', 'F9 i.i.d. fréq. allemandes', 'F10 i.i.d. fréq. bouteille']
def make(fam, text, bottle_freq, de_freq):
    o = R.randrange(len(text) - N - 50); x = text[o:o + N]
    f = {'F1 clair': lambda x: x, 'F2 substitution': sub, 'F3 Vigenère': vig, 'F4 transposition': colt,
         'F5 subst+transp': lambda x: colt(sub(x)), 'F6 Playfair': playfair, 'F7 Bifid': bifid, 'F8 homophonique': homoph,
         'F9 i.i.d. fréq. allemandes': iid(de_freq), 'F10 i.i.d. fréq. bouteille': iid(bottle_freq)}[fam]
    return np.asarray(f(x))[:N]

def bottle():
    import k02_contacts as k
    secs, _ = k.load_real(); return np.concatenate([np.array(s) for s in secs])

def distributions(nsamp=1000):
    b = bottle(); bf = np.bincount(b, minlength=26) / len(b); texts = {'de': load('de'), 'nl': load('nl')}
    df = np.bincount(texts['de'], minlength=26) / len(texts['de'])
    D = {}
    for fam in FAMS:
        D[fam] = np.array([stats(make(fam, texts['de' if i % 2 == 0 else 'nl'], bf, df)) for i in range(nsamp)])
    return D, b, bf, df, texts

def compat(v, dist):
    lo, hi = np.percentile(dist, 0.25, axis=0), np.percentile(dist, 99.75, axis=0)
    return (v >= lo) & (v <= hi)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    D, b, bf, df, texts = distributions()
    if mode == 'controles':
        extra = {fam: np.array([stats(make(fam, texts['de' if i % 2 else 'nl'], bf, df)) for i in range(40)]) for fam in FAMS}
        print('auto-compatibilité (≥ 90 % exigé) :')
        for fam in FAMS:
            print(f"  {fam:28s} {np.mean([compat(v, D[fam]).all() for v in extra[fam]]):.2f}")
        print('matrice : part des échantillons de la famille (ligne) jugés compatibles avec la famille (colonne)')
        print(' ' * 29 + ' '.join(f'{f.split()[0]:>5s}' for f in FAMS))
        for fa in FAMS:
            print(f"  {fa:27s} " + ' '.join(f"{np.mean([compat(v, D[fb]).all() for v in extra[fa]]):5.2f}" for fb in FAMS))
    else:
        v = stats(b)
        print('bouteille : ' + ', '.join(f"{n} {x:.4f}" for n, x in zip(NAMES, v)))
        for fam in FAMS:
            ok = compat(v, D[fam]); pct = [(D[fam][:, j] < v[j]).mean() * 100 for j in range(len(v))]
            bad = [f"{NAMES[j]} (centile {pct[j]:.1f})" for j in range(len(v)) if not ok[j]]
            print(f"  {fam:28s} {'COMPATIBLE' if ok.all() else 'exclue : ' + ', '.join(bad)}")
