"""Contrôle planté BLUME : deux clairs espagnols (n1, n2 lettres) d'un texte réservé, chiffrés par double transposition
directe avec les MÊMES clés-phrases K1, K2 (rang alphabétique, ex aequo de gauche à droite ; conventions de bdt.c).
Usage : python3 plant2.py texte.txt n1 n2 K1 K2 graine sortie1 sortie2"""
import sys, random
txt = open(sys.argv[1]).read().strip(); n1, n2 = int(sys.argv[2]), int(sys.argv[3]); K1, K2 = sys.argv[4], sys.argv[5]
rnd = random.Random(int(sys.argv[6])); o1 = rnd.randrange(len(txt) - n1 - n2 - 10000); o2 = o1 + n1 + rnd.randrange(5000)
import os
TIES = os.environ.get('PLANT_TIES') == '1'   # ex aequo de droite à gauche
def order(k): return [i for r in 'abcdefghijklmnopqrstuvwxyz' for i, ch in (reversed(list(enumerate(k))) if TIES else enumerate(k)) if ch == r]
def mapping(n, w, perm):
    h, r = divmod(n, w); start = [0] * w; pos = 0
    for j in range(w): col = perm[j]; start[col] = pos; pos += h + (col < r)
    return [start[i % w] + i // w for i in range(n)]
def enc(P):
    n = len(P); p1 = mapping(n, len(K1), order(K1)); p2 = mapping(n, len(K2), order(K2)); t = [''] * n; c = [''] * n
    for i in range(n): t[p1[i]] = P[i]
    for j in range(n): c[p2[j]] = t[j]
    return ''.join(c)
open(sys.argv[7], 'w').write(enc(txt[o1:o1 + n1]) + '\n'); open(sys.argv[8], 'w').write(enc(txt[o2:o2 + n2]) + '\n')
print('clair 1 :', txt[o1:o1 + 50])
