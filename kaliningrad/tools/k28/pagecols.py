"""K28 complément — lecture « en colonnes » de la page manuscrite elle-même.
Les routes de K06 portent sur le flux découpé en largeurs fixes ; ici les lignes réelles (35 à 46 lettres) servent de
rangées : on lit la k-ième lettre de chaque ligne, k = 1, 2, … (de haut en bas, ou de bas en haut, en alternance ou
non), page 1 seule (L01–L20), page 2 seule, ou les deux ; position comptée en lettres, ou en caractères (espaces et
signes compris, ce qui suit l'alignement visuel). Note : quadrigrammes allemands ; témoins : 300 jeux de lignes de
mêmes longueurs remplies avec les lettres de la bouteille mélangées. Usage : python3 tools/k28/pagecols.py"""
import sys, random, re, numpy as np
sys.path.insert(0, 'tools/k18')
from common import lines_v1, tokens
QG = np.fromfile('data/models/qg_de.bin', dtype='<f4')
def score(s):
    a = np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64) - 97
    return float(QG[((a[:-3] * 26 + a[1:-2]) * 26 + a[2:-1]) * 26 + a[3:]].mean())
L = lines_v1()[:25]
def rows_letters(lines): return [''.join(tokens(l)) for l in lines]
def rows_chars(lines):
    out = []
    for l in lines:
        r = []
        for ch in l:
            t = tokens(ch); r.append(t[0] if t else None)
        out.append(r)
    return out
def read(rows, updown, snake):
    W = max(len(r) for r in rows); out = []
    for k in range(W):
        rr = rows if (updown == 0) ^ (snake and k % 2 == 1) else rows[::-1]
        for r in rr:
            if k < len(r) and r[k]: out.append(r[k])
    return ''.join(out)
rnd = random.Random(11)
sets = {'page 1': L[:20], 'page 2': L[20:], 'pages 1+2': L}
print('%-10s %-10s %-22s %8s %8s %6s  %s' % ('lignes', 'position', 'lecture', 'bouteille', 'témoins', 'rang', 'début'))
for sname, lines in sets.items():
    for pname, rows in (('lettres', rows_letters(lines)), ('caractères', rows_chars(lines))):
        allc = [c for r in rows for c in r if c]
        for updown in (0, 1):
            for snake in (0, 1):
                s = read(rows, updown, snake); sb = score(s)
                ctrl = []
                for _ in range(300):
                    sh = allc[:]; rnd.shuffle(sh); it = iter(sh)
                    rr = [[(next(it) if c else None) for c in r] for r in rows]
                    ctrl.append(score(read(rr, updown, snake)))
                ctrl = np.array(ctrl)
                lab = ('bas→haut' if updown else 'haut→bas') + (', alterné' if snake else '')
                print('%-10s %-10s %-22s %8.3f %8.3f %6.2f  %s' % (sname, pname, lab, sb, ctrl.mean(), (ctrl >= sb).mean(), s[:40]))
