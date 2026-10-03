"""K28 — « eimat » (ou « Heimat ») comme clé : test direct sur les procédés classiques.
Chaque procédé est appliqué (dans les deux sens de lecture de la clé, déchiffrement ET chiffrement, texte entier et
par bloc) à la bouteille et à 300 mélanges de ses lettres ; note : quadrigrammes allemands moyens (qg_de.bin).
Un clair allemand obtient ≈ −9,5 à −10,5 (−11 avec 10 % de nuls) ; des lettres mélangées ≈ −14,3.
Usage : python3 tools/k28/eimat.py   (≈ 1 min)"""
import random, sys, numpy as np
QG = np.fromfile('data/models/qg_de.bin', dtype='<f4')
C = ''.join(ch for ch in open('data/ciphertext_979.txt').read() if 'a' <= ch <= 'z')
BL = [166, 169, 162, 169, 169, 144]
def score(s):
    a = np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64) - 97
    idx = ((a[:-3] * 26 + a[1:-2]) * 26 + a[2:-1]) * 26 + a[3:]
    return float(QG[idx].mean())
def ranks(k):
    o = sorted(range(len(k)), key=lambda i: (k[i], i)); r = [0] * len(k)
    for t, i in enumerate(o): r[i] = t
    return r
def enc_perm(r, inv, L):
    n = len(r); order = [0] * n
    for c in range(n):
        if inv: order[c] = r[c]
        else: order[r[c]] = c
    return [i for t in range(n) for i in range(order[t], L, n)]
def col_dec(s, r, inv):
    e = enc_perm(r, inv, len(s)); P = [''] * len(s)
    for j, i in enumerate(e): P[i] = s[j]
    return ''.join(P)
def col_enc(s, r, inv): return ''.join(s[i] for i in enc_perm(r, inv, len(s)))
def vig(s, k, mode):
    out = []
    for i, ch in enumerate(s):
        c, kk = ord(ch) - 97, ord(k[i % len(k)]) - 97
        p = (c - kk) % 26 if mode == 'vig' else (kk - c) % 26 if mode == 'beau' else (c + kk) % 26
        out.append(chr(97 + p))
    return ''.join(out)
def rail(s, n, dec=True):
    L = len(s); pat = []
    for i in range(L):
        p = i % (2 * n - 2) if n > 1 else 0; pat.append(p if p < n else 2 * n - 2 - p)
    order = sorted(range(L), key=lambda i: (pat[i], i))
    if dec:
        P = [''] * L
        for j, i in enumerate(order): P[i] = s[j]
        return ''.join(P)
    return ''.join(s[i] for i in order)
def per_block(f):
    def g(s):
        o = 0; out = ''
        for b in BL: out += f(s[o:o + b]); o += b
        return out
    return g
methods = {}
for key in ('eimat', 'heimat', 'tamie', 'tamieh'):
    r = ranks(key)
    for inv in (0, 1):
        methods['colonnes déchiffr. %s v%d' % (key, inv)] = lambda s, r=r, inv=inv: col_dec(s, r, inv)
        methods['colonnes chiffr. %s v%d' % (key, inv)] = lambda s, r=r, inv=inv: col_enc(s, r, inv)
        methods['double (même clé) %s v%d' % (key, inv)] = lambda s, r=r, inv=inv: col_dec(col_dec(s, r, inv), r, inv)
        methods['colonnes par bloc %s v%d' % (key, inv)] = per_block(lambda s, r=r, inv=inv: col_dec(s, r, inv))
        methods['double par bloc %s v%d' % (key, inv)] = per_block(lambda s, r=r, inv=inv: col_dec(col_dec(s, r, inv), r, inv))
for key in ('eimat', 'heimat'):
    for mode in ('vig', 'beau', 'var'):
        methods['%s %s' % (mode, key)] = lambda s, key=key, mode=mode: vig(s, key, mode)
for n in (5, 6):
    methods['zigzag %d rails' % n] = lambda s, n=n: rail(s, n)
    methods['zigzag %d rails par bloc' % n] = per_block(lambda s, n=n: rail(s, n))
rnd = random.Random(2026)
shuf = []
for _ in range(300):
    x = list(C); rnd.shuffle(x); shuf.append(''.join(x))
best_any = []
print('%-34s %8s %8s %6s %s' % ('procédé', 'bouteille', 'mélanges', 'rang', 'début du résultat'))
for name, f in methods.items():
    sb = score(f(C)); ss = np.array([score(f(x)) for x in shuf])
    rank = (ss >= sb).mean()
    print('%-34s %8.3f %8.3f %6.2f %s' % (name, sb, ss.mean(), rank, f(C)[:50]))
print('\nrepère : bouteille telle quelle %.3f' % score(C))
