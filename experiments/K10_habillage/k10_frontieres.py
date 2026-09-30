#!/usr/bin/env python3
"""K10 — test des frontières de mots (ordre des mots mélangé) sur la bouteille et sur des textes réels.
Usage : python3 experiments/K10_habillage/k10_frontieres.py [dossiers de textes de contrôle ...]"""
import sys, os, re, glob, unicodedata
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = set('aeiouyаеёиоуыэюяäöü')
rng = np.random.default_rng(5)

def ws_bottle(lines):
    ws = [''.join({'ê': 'e', 'ö': 'o', 'ü': 'u'}.get(c, c) for c in w.lower() if c.isalpha() or c in 'êöü')
          for w in ' '.join(lines).replace('_', '').split()]
    return [w for w in ws if w]

def alt(o):
    return sum((a[-1] in V) != (b[0] in V) for a, b in zip(o[:-1], o[1:]))

def ztest(ws, n=20000):
    o = alt(ws); nul = np.array([alt([ws[i] for i in rng.permutation(len(ws))]) for _ in range(n)])
    return o, nul.mean(), (o - nul.mean()) / nul.std()

if __name__ == '__main__':
    v1 = [l[4:].rstrip() for l in open(os.path.join(ROOT, 'data', 'transcription_v1.txt'), encoding='utf-8') if l.startswith('L')][:25]
    cs = [l.rstrip() for l in open(os.path.join(ROOT, 'data', 'transcription_corsair_2015.txt'), encoding='utf-8')
          if not l.startswith('#') and l.strip()]
    cs = [l for l in cs[:25] if re.match(r"^[a-zA-Zêöü'\"\. ]+$", l) and not l.startswith('eimat')]
    for name, lines in (('v1 entier', v1), ('v1 page 1', v1[:20]), ('v1 page 2', v1[20:]), ('Corsair 2015', cs)):
        o, m, z = ztest(ws_bottle(lines)); print(f"{name:14s} C|V {o} vs {m:.1f}  z={z:+.1f}")
    for d in sys.argv[1:]:
        for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
            t = ''.join(c for c in unicodedata.normalize('NFD', open(f, encoding='utf-8', errors='ignore').read().lower())
                        if unicodedata.category(c) != 'Mn')
            ws = re.findall(r'[^\W\d_]+', t)[1000:]
            zs = [ztest(ws[s:s + 194], 300)[2] for s in range(0, min(len(ws) - 194, 194 * 60), 194)]
            if zs: print(f"{os.path.basename(f):16s} fenêtres {len(zs)} z moyen {np.mean(zs):+.2f} z min {np.min(zs):+.2f}")
