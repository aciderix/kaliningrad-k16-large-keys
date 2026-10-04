"""Contrôle planté pour les autres conventions de double transposition (mêmes clés pour T1 et T2).
F_K : écrire en lignes, lire les colonnes dans l'ordre de K ; G_K = F_K⁻¹. conv : fwd (F∘F), rev (G∘G),
cr (F_K2∘G_K1, colonnes puis lignes), rc (G_K2∘F_K1). Usage : python3 plant_conv.py texte n1 n2 K1 K2 conv graine s1 s2"""
import sys, random
txt = open(sys.argv[1]).read().strip(); n1, n2 = int(sys.argv[2]), int(sys.argv[3]); K1, K2, conv = sys.argv[4], sys.argv[5], sys.argv[6]
rnd = random.Random(int(sys.argv[7])); o1 = rnd.randrange(len(txt) - n1 - n2 - 10000); o2 = o1 + n1 + rnd.randrange(5000)
def order(k): return [i for r in 'abcdefghijklmnopqrstuvwxyz' for i, ch in enumerate(k) if ch == r]
def mapping(n, w, perm):
    h, r = divmod(n, w); start = [0] * w; pos = 0
    for j in range(w): col = perm[j]; start[col] = pos; pos += h + (col < r)
    return [start[i % w] + i // w for i in range(n)]
def F(x, K):
    p = mapping(len(x), len(K), order(K)); out = [''] * len(x)
    for i in range(len(x)): out[p[i]] = x[i]
    return ''.join(out)
def G(x, K):
    p = mapping(len(x), len(K), order(K)); return ''.join(x[p[i]] for i in range(len(x)))
def enc(P):
    return {'fwd': lambda: F(F(P, K1), K2), 'rev': lambda: G(G(P, K1), K2), 'cr': lambda: F(G(P, K1), K2), 'rc': lambda: G(F(P, K1), K2)}[conv]()
open(sys.argv[8], 'w').write(enc(txt[o1:o1 + n1]) + '\n'); open(sys.argv[9], 'w').write(enc(txt[o2:o2 + n2]) + '\n')
print('clair 1 :', txt[o1:o1 + 60])
