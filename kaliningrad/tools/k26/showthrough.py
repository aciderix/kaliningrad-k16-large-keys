"""K26 — Les lignes délavées du bas de la page 2 sont-elles un texte caché ?
Compare, ligne par ligne, le profil horizontal d'encre bleue de chaque ligne délavée de la page 2 avec celui de
chaque ligne de la page 1, à l'endroit et en miroir (une transparence vue du verso serait inversée).
Photos (non versées) : K. Schmeh, Cipherbrain 2016, 688 × 841 px :
  curl -O https://scienceblogs.de/klausis-krypto-kolumne/files/2016/09/Kaliningrad-Cryptogram1.png
  curl -O https://scienceblogs.de/klausis-krypto-kolumne/files/2016/09/Kaliningrad-Cryptogram-2.png
Usage : python3 tools/k26/showthrough.py <dossier des photos>   (nécessite numpy, pillow)
"""
import sys, os
import numpy as np
from PIL import Image
D = sys.argv[1] if len(sys.argv) > 1 else '.'
def ink(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    x = a[..., 2] - a[..., 0]                       # encre bleue : B - R
    lo, hi = np.percentile(x, 5), np.percentile(x, 99.5)
    return np.clip((x - lo) / (hi - lo), 0, 1)
p1 = ink(os.path.join(D, 'Kaliningrad-Cryptogram1.png'))
p2 = ink(os.path.join(D, 'Kaliningrad-Cryptogram-2.png'))
def peaks(img, lo, hi):
    prof = np.convolve(img.mean(1), np.ones(9) / 9, 'same')
    ys = [y for y in range(lo + 10, hi - 10) if prof[y] == prof[y - 10:y + 11].max() and prof[y] > 0.12]
    out = []
    for y in ys:
        if not out or y - out[-1] > 15: out.append(y)
    return out
X0, X1 = 25, 665
def colprof(img, y, h=11):
    c = np.convolve(img[y - h:y + h, X0:X1].mean(0), np.ones(9) / 9, 'same')
    return (c - c.mean()) / (c.std() + 1e-9)
def best(a, b, m=60):
    r = -9; s0 = 0
    for s in range(-m, m + 1):
        aa, bb = (a[s:], b[:len(b) - s]) if s >= 0 else (a[:s], b[-s:])
        c = np.corrcoef(aa, bb)[0, 1]
        if c > r: r, s0 = c, s
    return r, s0
y1 = peaks(p1, 60, 780)
y2 = [y for y in peaks(p2, 60, 790) if y > 275]     # sous « eimat » : lignes délavées
print('page 1 : %d lignes, y =' % len(y1), y1)
print('page 2 (sous eimat) : %d lignes délavées, y =' % len(y2), y2)
P1 = [colprof(p1, y) for y in y1]
for mode in ('endroit', 'miroir'):
    print('\n== page 1 %s' % mode)
    same = []
    for y in y2:
        c2 = colprof(p2, y)
        rs = sorted(((best(c2, c[::-1] if mode == 'miroir' else c), k + 1) for k, c in enumerate(P1)), reverse=True)
        k_same = int(np.argmin([abs(y - v) for v in y1])) + 1      # ligne de la page 1 à la même hauteur
        r_same = [r for (r, s), k in rs if k == k_same][0]
        same.append(r_same)
        print('p2 y=%3d  même hauteur L%02d r=%.2f | meilleures : %s' % (y, k_same, r_same,
              ' '.join('L%02d %.2f (décalage %+d)' % (k, r, s) for (r, s), k in rs[:3])))
    print('médiane r (ligne de même hauteur) = %.2f' % np.median(same))
