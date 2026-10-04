#!/usr/bin/env python3
"""K17 — tests invariants par transposition : le flux peut-il être un texte allemand remis en désordre ?

Une transposition (simple, double, grille, route, quelle que soit la clé) déplace les lettres sans les changer :
le nombre de chaque lettre du clair est exactement celui du chiffré. On compare donc le décompte du flux aux
fenêtres de 979 lettres de textes allemands réels ; la distribution de ces fenêtres est le contrôle (un vrai
texte allemand transposé a, par construction, le décompte d'une de ces fenêtres). Aucune clé n'est cherchée.

Usage : python3 tools/k17_profil.py [dossier_de_textes_supplémentaires_de]
"""
import glob
import math
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path

A = "abcdefghijklmnopqrstuvwxyz"


def clean(s):
    s = s.lower().replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "".join(c for c in s if c in A)


def gutenberg_body(raw):
    a, b = raw.find("*** START"), raw.find("*** END")
    return raw[a + 200:b] if 0 < a < b else raw


C = Path("data/ciphertext_979.txt").read_text().strip()
N = len(C)
cc = Counter(C)
bc = [cc[a] for a in A]

ref = clean(Path("data/heldout/de.txt").read_text(encoding="utf-8"))
ref += clean("".join(l for l in open("data/controle_de_kant_6343.txt", encoding="utf-8") if not l.startswith("#")))
if len(sys.argv) > 1:
    for f in sorted(glob.glob(str(Path(sys.argv[1]) / "*.txt"))):
        ref += clean(gutenberg_body(open(f, encoding="utf-8", errors="ignore").read()))
ct = Counter(ref)
p = [(ct[a] + 0.5) / (len(ref) + 13) for a in A]
step = N // 4
windows = [[Counter(ref[s:s + N])[a] for a in A] for s in range(0, len(ref) - N, step)]
print(f"flux : {N} lettres ; référence allemande : {len(ref)} lettres, {len(windows)} fenêtres de {N} (pas {step})\n")


def G(counts, probs):
    return 2 * sum(c * math.log(c / (N * q)) for c, q in zip(counts, probs) if c > 0)


# T1 — transposition pure : décompte des lettres
print("T1  transposition seule (lettres intactes)")
print("    lettre  flux  attendu  z")
for i, a in enumerate(A):
    e = N * p[i]
    z = (bc[i] - e) / math.sqrt(e * (1 - p[i]))
    if abs(z) >= 2:
        print(f"    {a}      {bc[i]:4d}  {e:7.1f}  {z:+.1f}")
gb = G(bc, p)
gw = [G(w, p) for w in windows]
print(f"    G flux = {gb:.1f} ; fenêtres allemandes >= flux : {sum(g >= gb for g in gw)}/{len(gw)} (max {max(gw):.1f})")
fw = cc["f"] + cc["w"]
fww = [w[A.index("f")] + w[A.index("w")] for w in windows]
print(f"    f+w flux = {fw} ; fenêtres : max {max(fww)}")

# T2 — transposition + substitution simple : profil trié
print("\nT2  transposition + substitution (profil trié)")
ps = sorted(p, reverse=True)
gs = lambda counts: G(sorted(counts, reverse=True), ps)
gsb = gs(bc)
gsw = [gs(w) for w in windows]
print(f"    G trié flux = {gsb:.1f} ; fenêtres >= flux : {sum(g >= gsb for g in gsw)}/{len(gsw)} (max {max(gsw):.1f})")

# T3 — les lettres sont-elles leurs propres lettres (pas de substitution) ?
print("\nT3  identité des lettres contre étiquetage aléatoire")
lp = [math.log(x) for x in p]
ll = lambda counts: sum(c * l for c, l in zip(counts, lp))
rng = random.Random(17)
R = 100000
idll = ll(bc)
hits = 0
q = bc[:]
for _ in range(R):
    rng.shuffle(q)
    hits += ll(q) >= idll
print(f"    étiquetages aléatoires aussi proches de l'allemand que l'identité : {hits}/{R}")
print(f"    lettres absentes du flux : {[a for a in A if cc[a] == 0]} ; plus rares en allemand : {sorted(A, key=lambda a: ct[a])[:4]}")
