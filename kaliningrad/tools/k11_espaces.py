#!/usr/bin/env python3
"""K11 — identification de la règle de placement des espaces (voir experiments/K11_regle_des_espaces/PREREGISTRATION.md).
Usage : python3 tools/k11_espaces.py [controles|reel] [nnull]"""
import sys, os, re, random, unicodedata
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AL = 'abcdefghijklmnopqrstuvwxyz'; IDX = {c: i for i, c in enumerate(AL)}; VOW = set('aeiouyаеёиоуыэюя')
CYR = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
R = random.Random(1111); NR = np.random.default_rng(1111)
SCRATCH_LANG = os.environ.get('K11_LANG', '')

# ---------- données : liste de lignes, chaque ligne = liste de mots (mot = (lettres, abrev?)) ----------
def norm_word(w):
    return ''.join({'ê': 'e', 'ö': 'o', 'ü': 'u'}.get(c, c) for c in w.lower() if c.isalpha() or c in 'êöü')

def lines_bottle(path, corsair=False):
    raw = [l.rstrip('\n') for l in open(path, encoding='utf-8')]
    if corsair:
        raw = [l for l in raw if not l.startswith('#') and l.strip()][:25]
        raw = [l for l in raw if re.match(r"^[a-zA-Zêöü'\"\. ]+$", l) and not l.startswith('eimat')]
    else:
        raw = [l[4:] for l in raw if l.startswith('L')][:25]
    out = []
    for l in raw:
        ws = []
        for tok in l.replace('_', '').split():
            w = norm_word(tok)
            if w: ws.append((w, bool(re.fullmatch(r"([a-zA-Z]\.'?)+", tok))))
        out.append(ws)
    return out

# ---------- jonctions et variables ----------
def junctions(lines):
    rows = []
    for li, ws in enumerate(lines):
        stream = []; cut_after = []; excl = []
        for wi, (w, ab) in enumerate(ws):
            for ci, ch in enumerate(w):
                stream.append(ch)
                last = ci == len(w) - 1
                cut_after.append(last); excl.append(ab and not last)
        n = len(stream); pos_in_word = 0
        for i in range(n - 1):
            pos_in_word += 1
            if not excl[i]:
                a, b = stream[i], stream[i + 1]
                a2 = stream[i - 1] if i > 0 else None; b2 = stream[i + 2] if i + 2 < n else None
                rows.append((li, a, b, a2, b2, min(pos_in_word, 8), int(3 * i / max(1, n - 1)), int(cut_after[i])))
            if cut_after[i]: pos_in_word = 0
    return rows

def features(rows, model):
    X = []
    for (li, a, b, a2, b2, L, third, y) in rows:
        f = [1.0] + [1.0 if L == k else 0.0 for k in range(2, 9)]
        va, vb = a in VOW, b in VOW
        if model in ('M1', 'M2', 'M5', 'M6'):
            f += [float(va), float(vb)]
        if model in ('M3', 'M4'):
            alph = CYR if (a in CYR or b in CYR) else AL
            f += [1.0 if a == c else 0.0 for c in alph] + [1.0 if b == c else 0.0 for c in alph]
        if model in ('M2', 'M4', 'M5', 'M6'):
            f += [float(va and vb), float((not va) and (not vb)), float(a == b)]
        if model == 'M5':
            v2a = a2 in VOW if a2 else False; v2b = b2 in VOW if b2 else False
            f += [float(a2 is not None and v2a), float(b2 is not None and v2b),
                  float(a2 is not None and (not v2a) and (not va)), float(b2 is not None and (not v2b) and (not vb)),
                  float(a2 is not None and v2a and va), float(b2 is not None and v2b and vb)]
        if model == 'M6':
            f += [1.0 if third == 1 else 0.0, 1.0 if third == 2 else 0.0]
        X.append(f)
    return np.array(X), np.array([r[7] for r in rows], dtype=float)

def fit(X, y, lam=1.0, it=50):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ w)); W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + lam * np.eye(X.shape[1]); H[0, 0] -= lam
        g = X.T @ (y - p) - lam * w; g[0] += lam * w[0]
        step = np.linalg.solve(H, g); w += step
        if np.abs(step).max() < 1e-8: break
    return w

def ll(X, y, w):
    p = np.clip(1 / (1 + np.exp(-X @ w)), 1e-12, 1 - 1e-12)
    return float((y * np.log(p) + (1 - y) * np.log(1 - p)).sum())

MODELS = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6']
def cv_ll(lines):
    rows = junctions(lines); out = {}
    for m in MODELS:
        X, y = features(rows, m); odd = np.array([r[0] % 2 == 1 for r in rows]); tot = 0.0
        for tr in (odd, ~odd):
            w = fit(X[tr], y[tr]); tot += ll(X[~tr], y[~tr], w)
        out[m] = tot
    return out

def gains(lines):
    c = cv_ll(lines)
    return {'G_int': c['M2'] - c['M1'], "G'_int": c['M4'] - c['M3'], 'G_fen': c['M5'] - c['M2'], 'G_pos': c['M6'] - c['M2']}, c

def shuffle_words(lines):
    allw = [w for ws in lines for w in ws]; R.shuffle(allw); out = []; k = 0
    for ws in lines: out.append(allw[k:k + len(ws)]); k += len(ws)
    return out

def test(lines, nnull, label):
    g, c = gains(lines); nul = {k: [] for k in g}
    for _ in range(nnull):
        gg, _ = gains(shuffle_words(lines))
        for kk in g: nul[kk].append(gg[kk])
    ps = {kk: (sum(x >= g[kk] for x in nul[kk]) + 1) / (nnull + 1) for kk in g}
    print(f"[{label}] " + ' ; '.join(f"{kk} = {g[kk]:+.2f} (nul moy {np.mean(nul[kk]):+.2f}, p = {ps[kk]:.3f})" for kk in g), flush=True)
    return g, ps, c

# ---------- générateurs pour les contrôles ----------
LEN_F = [0.25, 0.7, 1.0, 1.2, 1.4, 1.6, 2.0, 3.0]
def planted(letters, rule):
    """rule 'int' : taux par catégorie de paire (K10) ; rule 'add' : produit d'effets séparés (sans interaction)."""
    ws = []; cur = ''
    for i, ch in enumerate(letters):
        cur += ch
        if i + 1 == len(letters): break
        a, b = ch, letters[i + 1]; va, vb = a in VOW, b in VOW
        if rule == 'int':
            base = 0.55 if a == b and va else 0.21 if a == b else 0.31 if va and vb else 0.23 if not va and not vb else 0.106
        else:
            base = (0.24 if va else 0.18) * (1.05 if vb else 0.95)
        p = min(0.95, base * LEN_F[min(len(cur), 8) - 1] / 1.1)
        if R.random() < p: ws.append((cur, False)); cur = ''
    ws.append((cur, False))
    return reflow(ws)

def reflow(ws, width=40):
    lines = []; cur = []; n = 0
    for w in ws:
        if n + len(w[0]) > width and cur: lines.append(cur); cur = []; n = 0
        cur.append(w); n += len(w[0])
    if cur: lines.append(cur)
    return lines

def real_windows(path, nwin=10, nlet=980):
    t = ''.join(c for c in unicodedata.normalize('NFD', open(path, encoding='utf-8', errors='ignore').read().lower())
                if unicodedata.category(c) != 'Mn')
    t = t.replace('ß', 'ss')
    words = [w for w in re.findall(r'[^\W\d_]+', t)][2000:]
    out = []; k = 0; gap = max(0, (len(words) - nwin * 250) // nwin)
    for _ in range(nwin):
        ws = []; n = 0
        while n < nlet: ws.append((words[k], False)); n += len(words[k]); k += 1
        k += gap
        out.append(reflow(ws))
    return out

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    nnull = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    if mode == 'controles':
        if os.environ.get('K11_SKIP_PLANTED'): base = None
        else: base = [ch for ws in lines_bottle(os.path.join(ROOT, 'data', 'transcription_v1.txt')) for w, ab in ws for ch in w]
        for rule in (('int', 'add') if base else ()):
            hits = 0
            for t in range(10):
                L = base[:]; R.shuffle(L)
                g, ps, _ = test(planted(L, rule), nnull, f"planté {rule} {t}")
                hits += ps['G_int'] < 0.01
            print(f"==> règle planté '{rule}' : G_int p < 0,01 dans {hits}/10", flush=True)
        for f in SCRATCH_LANG.split(','):
            if not f: continue
            ok = 0
            for t, lines in enumerate(real_windows(f)):
                g, ps, _ = test(lines, nnull, f"{os.path.basename(f)} fenêtre {t}")
                ok += ps['G_int'] > 0.01
            print(f"==> {os.path.basename(f)} : G_int au niveau du nul (p > 0,01) dans {ok}/10", flush=True)
    else:
        for label, lines in (('v1', lines_bottle(os.path.join(ROOT, 'data', 'transcription_v1.txt'))),
                             ('v1 page 1', lines_bottle(os.path.join(ROOT, 'data', 'transcription_v1.txt'))[:20]),
                             ('Corsair 2015', lines_bottle(os.path.join(ROOT, 'data', 'transcription_corsair_2015.txt'), corsair=True))):
            g, ps, c = test(lines, nnull, label)
            print('    LL hors échantillon : ' + ', '.join(f"{m} {c[m]:.1f}" for m in MODELS), flush=True)
        # paramètres de la règle M2 ajustée sur tout v1
        rows = junctions(lines_bottle(os.path.join(ROOT, 'data', 'transcription_v1.txt')))
        X, y = features(rows, 'M2'); w = fit(X, y)
        names = ['const'] + [f'L={k}' for k in range(2, 9)] + ['avant=V', 'après=V', 'V|V', 'C|C', 'identiques']
        print('    M2 (log-odds) : ' + ', '.join(f"{n} {v:+.2f}" for n, v in zip(names, w)))
