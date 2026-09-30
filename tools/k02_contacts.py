#!/usr/bin/env python3
"""K02 — contacts entre lettres (T5) et réalité des espaces (T6). Voir experiments/K02_contacts/PREREGISTRATION.md.
Usage : python3 tools/k02_contacts.py [controles|reel]"""
import sys, os, re, random
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = random.Random(2027); NR = np.random.default_rng(2027)
AL = 'abcdefghijklmnopqrstuvwxyz'; IDX = {c: i for i, c in enumerate(AL)}
SIZES = [166, 169, 162, 169, 169, 144]
DMAX, NPERM = 40, 2000
ACC = {'ê': 'e', 'ö': 'o', 'ü': 'u', 'ä': 'a', 'ß': 's', 'é': 'e'}

def norm(w):
    return ''.join(ACC.get(c, c) for c in w.lower() if ACC.get(c, c) in IDX)

def load_real():
    """Sections (listes d'indices de lettres) et mots (texte entier, jetons séparés par des espaces)."""
    L = [l[4:].rstrip('\n') for l in open(os.path.join(ROOT, 'data', 'transcription_v1.txt'), encoding='utf-8') if l.startswith('L')]
    t = ' '.join(L)
    secs, cur = [], []
    for tok in re.findall(r"[a-zA-Zêöü]_?", t):
        c = norm(tok[0])
        cur.append(IDX[c])
        if tok.endswith('_'):
            secs.append(cur); cur = []
    secs.append(cur)
    words = [w for w in (norm(x) for x in t.split()) if w]
    return secs[:6], words

def mi(counts):
    n = counts.sum(); p = counts / n
    px = p.sum(1, keepdims=True); py = p.sum(0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log2(p[nz] / (px @ py)[nz])).sum())

def mi_profile(secs):
    out = np.zeros(DMAX + 1)
    for d in range(1, DMAX + 1):
        codes = np.concatenate([s[:-d] * 26 + s[d:] for s in secs if len(s) > d])
        out[d] = mi(np.bincount(codes, minlength=676).reshape(26, 26).astype(float))
    return out

def t5(secs, name):
    secs = [np.array(s) for s in secs]
    obs = mi_profile(secs); null = np.zeros((NPERM, DMAX + 1))
    for k in range(NPERM):
        null[k] = mi_profile([NR.permutation(s) for s in secs])
    mu, sd = null.mean(0), null.std(0)
    p = ((null >= obs).sum(0) + 1) / (NPERM + 1)
    z = (obs - mu) / np.where(sd > 0, sd, 1)
    top = sorted(range(1, DMAX + 1), key=lambda d: -z[d])[:4]
    print(f"  [{name}] T5 p(1)={p[1]:.4f} z(1)={z[1]:.1f} | p(2)={p[2]:.4f} | p(12)={p[12]:.4f} p(13)={p[13]:.4f} z(13)={z[13]:.1f} | "
          f"plus forts z : " + ', '.join(f"d={d}:{z[d]:.1f}(p={p[d]:.4f})" for d in top))
    return p, z

def pos_table(words):
    tab = np.zeros((26, 4))
    for w in words:
        if len(w) == 1: tab[IDX[w], 3] += 1; continue
        tab[IDX[w[0]], 0] += 1; tab[IDX[w[-1]], 1] += 1
        for c in w[1:-1]: tab[IDX[c], 2] += 1
    return tab

def chi2(tab):
    tab = tab[tab.sum(1) > 0]
    e = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    m = e > 0
    return float(((tab - e)[m] ** 2 / e[m]).sum())

def t6(words, name):
    letters = ''.join(words); lens = [len(w) for w in words]
    obs = chi2(pos_table(words)); n = 0
    for _ in range(NPERM):
        R.shuffle(lens); k = 0; ws = []
        for l in lens: ws.append(letters[k:k + l]); k += l
        n += chi2(pos_table(ws)) >= obs
    print(f"  [{name}] T6 χ²={obs:.1f} p={(n + 1) / (NPERM + 1):.4f} (mots={len(words)})")

def split_sizes(seq):
    out, k = [], 0
    for s in SIZES: out.append(list(seq[k:k + s])); k += s
    return out

def columnar(sec, keyed):
    q = 12 if len(sec) <= 144 else 13
    rows = [sec[i:i + q] for i in range(0, len(sec), q)]
    order = list(range(q))
    if keyed: R.shuffle(order)
    return [r[c] for c in order for r in rows if c < len(r)]

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    if mode == 'controles':
        raw = open(os.path.join(ROOT, 'data', 'controle_de_kant_6343.txt'), encoding='utf-8').read().split('\n', 1)[1]
        gw = [w for w in (norm(x) for x in re.findall(r"\w+", raw)) if w]
        o = 0; seq = [IDX[c] for c in ''.join(gw)][o:o + 984]
        sub = list(range(26)); R.shuffle(sub)
        t5(split_sizes(seq), "(a) clair")
        t5(split_sizes([sub[c] for c in seq]), "(b) substitution simple")
        cK = [columnar(s, True) for s in split_sizes(seq)]
        t5(cK, "(c) carrés, colonnes à clé")
        t5([columnar(s, False) for s in split_sizes(seq)], "(d) carrés, colonnes dans l'ordre")
        sw = []; n = 0
        for w in gw:
            sw.append(''.join(AL[sub[IDX[c]]] for c in w)); n += len(w)
            if n >= 984: break
        t6(sw, "(e) mots allemands réels sous substitution")
        _, rw = load_real(); flat = ''.join(AL[c] for s in cK for c in s); ws = []; k = 0
        for w in rw:
            if k + len(w) > len(flat): break
            ws.append(flat[k:k + len(w)]); k += len(w)
        t6(ws, "(f) texte (c) recoupé avec les longueurs de mots du cryptogramme")
    else:
        secs, words = load_real()
        print("sections :", [len(s) for s in secs], "; mots :", len(words))
        t5(secs, "réel S1-S6")
        t5(secs[:5], "réel S1-S5")
        t5([secs[5]], "réel S6 seule (carré 12 ?)")
        t6(words, "réel")
