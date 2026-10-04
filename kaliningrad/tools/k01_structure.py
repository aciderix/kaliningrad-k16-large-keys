#!/usr/bin/env python3
"""K01 — tests de structure (voir experiments/K01_structure/PREREGISTRATION.md).
Usage : python3 tools/k01_structure.py [controles|reel] [v1|v0]"""
import sys, os, re, random, collections, math
import wordfreq
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = random.Random(2026)
AL = 'abcdefghijklmnopqrstuvwxyz'
NPERM = 10000

def load_real(ver='v1'):
    L = [l[4:].rstrip('\n') for l in open(os.path.join(ROOT, 'data', f'transcription_{ver}.txt'), encoding='utf-8') if l.startswith('L')]
    t = ' '.join(L)
    # sections (variante A) et mots
    secs, cur = [], []
    for tok in re.findall(r"[a-zA-Zêöü]_?|[.'\"~ ]", t):
        if tok[0].isalpha():
            c = {'ê': 'e', 'ö': 'o', 'ü': 'u'}.get(tok[0].lower(), tok[0].lower())
            cur.append(c)
            if tok.endswith('_'):
                secs.append(cur); cur = []
    secs.append(cur)
    words = []
    for w in t.split():
        if '.' in w.strip('.') or re.fullmatch(r"(\w\.)+", w):  # abréviations x.s.f.d.
            continue
        w2 = ''.join({'ê': 'e', 'ö': 'o', 'ü': 'u'}.get(ch, ch) for ch in w.lower() if ch.isalpha() or ch in 'êöü')
        if w2: words.append(w2)
    return secs, words

def chi2_homog(blocks):
    tot = collections.Counter(); n = [len(b) for b in blocks]; N = sum(n)
    cnts = [collections.Counter(b) for b in blocks]
    for c in cnts: tot.update(c)
    s = 0.0
    for k in tot:
        for c, nb in zip(cnts, n):
            e = tot[k] * nb / N
            s += (c[k] - e) ** 2 / e
    return s

def sorted_prof_dist(blocks):
    profs = []
    for b in blocks:
        c = sorted(collections.Counter(b).values(), reverse=True) + [0] * 30
        profs.append([x / len(b) for x in c[:30]])
    d = 0.0
    for i in range(len(profs)):
        for j in range(i + 1, len(profs)):
            d += sum(abs(a - b) for a, b in zip(profs[i], profs[j]))
    return d

def iso_score(blocks, dmax=10, win=20):
    best = 0
    for a in range(len(blocks)):
        for b in range(a + 1, len(blocks)):
            A, B = blocks[a], blocks[b]
            for d in range(-dmax, dmax + 1):
                s = 0
                for i in range(len(A)):
                    for j in range(i + 1, min(len(A), i + win + 1)):
                        ib, jb = i + d, j + d
                        if 0 <= ib < len(B) and 0 <= jb < len(B) and A[i] == A[j] and B[ib] == B[jb]:
                            s += 1
                best = max(best, s)
    return best

def perm_tests(blocks, name, niso=300):
    sizes = [len(b) for b in blocks]; allc = [c for b in blocks for c in b]
    o1, o2, o3 = chi2_homog(blocks), sorted_prof_dist(blocks), iso_score(blocks)
    n1 = n2 = n3 = 0; n1h = 0
    for t in range(NPERM):
        R.shuffle(allc); k = 0; bl = []
        for s in sizes: bl.append(allc[k:k + s]); k += s
        v1 = chi2_homog(bl); n1 += v1 <= o1; n1h += v1 >= o1
        n2 += sorted_prof_dist(bl) <= o2
        if t < niso: n3 += iso_score(bl) >= o3
    print(f"  [{name}] T1 χ²={o1:.1f} p_bas={(n1+1)/(NPERM+1):.4f} p_haut={(n1h+1)/(NPERM+1):.4f} | "
          f"T2 dist={o2:.3f} p_bas={(n2+1)/(NPERM+1):.4f} | T3 iso={o3} p_haut={(n3+1)/(niso+1):.4f}")

LEX = {}
def lexicon(lang):
    if lang not in LEX:
        keys = set()
        for w in wordfreq.top_n_list(lang, 50000):
            w = w.lower().replace('ß', 'ss')
            w = ''.join({'ä': 'a', 'ö': 'o', 'ü': 'u', 'é': 'e', 'è': 'e', 'à': 'a', 'å': 'a', 'ø': 'o', 'æ': 'ae', 'ł': 'l'}.get(c, c) for c in w)
            w = ''.join(c for c in w if c in AL)
            if len(w) >= 4: keys.add(''.join(sorted(w)))
        LEX[lang] = keys
    return LEX[lang]

LANGS = ['de', 'nl', 'en', 'sv', 'da', 'cs', 'pl', 'fr', 'it']
def anagram_test(words, name, freqsrc):
    ws = [w for w in words if len(w) >= 4]
    fq = collections.Counter(c for w in freqsrc for c in w); letters = list(fq.keys()); weights = [fq[c] for c in letters]
    out = []
    for lang in LANGS:
        lx = lexicon(lang)
        f = sum(''.join(sorted(w)) in lx for w in ws) / len(ws)
        # null : mots aléatoires de mêmes longueurs, lettres selon les fréquences du texte
        nulls = []
        for _ in range(200):
            nulls.append(sum(''.join(sorted(R.choices(letters, weights, k=len(w)))) in lx for w in ws) / len(ws))
        m = sum(nulls) / len(nulls); p = (sum(x >= f for x in nulls) + 1) / 201
        out.append(f"{lang}:{f:.3f}(null {m:.3f}, p={p:.3f})")
    print(f"  [{name}] T4 mots≥4 = {len(ws)} ; " + ' '.join(out))

def german_text():
    t = open(os.path.join(ROOT, '..', 'dagapeyeff', 'data', 'heldout', 'de.txt')).read().lower()
    return [c for c in t if c in AL]

def german_words(n):
    w = wordfreq.top_n_list('de', 20000); p = [wordfreq.word_frequency(x, 'de') for x in w]
    out = []
    while sum(len(x) for x in out) < n:
        x = R.choices(w, p)[0].replace('ß', 'ss'); x = ''.join({'ä': 'a', 'ö': 'o', 'ü': 'u'}.get(c, c) for c in x)
        x = ''.join(c for c in x if c in AL)
        if x: out.append(x)
    return out

def randsub():
    p = list(AL); R.shuffle(p); return dict(zip(AL, p))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'controles'
    if mode == 'controles':
        G = german_text(); o = R.randrange(len(G) - 5000); sizes = [166, 169, 162, 169, 169, 144]
        base = G[o:o + 170]
        a = []
        for s in sizes:
            b = base[:s]; b = b[:]; R.shuffle(b); a.append(b)
        perm_tests(a, "(a) même bloc transposé 6 fois")
        b = []
        for s in sizes:
            m = randsub(); b.append([m[c] for c in base[:s]])
        perm_tests(b, "(b) même bloc, 6 substitutions")
        m = randsub(); k = o + 500; c = []
        for s in sizes: c.append([m[x] for x in G[k:k + s]]); k += s
        perm_tests(c, "(c) 6 blocs différents, même substitution")
        gw = german_words(1000)
        anag = [''.join(R.sample(w, len(w))) for w in gw]
        anagram_test(anag, "(d) mots allemands anagrammés", anag)
        m = randsub(); subw = [''.join(m[ch] for ch in w) for w in gw]
        anagram_test(subw, "(e) mots allemands substitués", subw)
    else:
        secs, words = load_real(sys.argv[2] if len(sys.argv) > 2 else 'v1')
        full = secs[:6]
        print("sections (variante A) :", [len(s) for s in secs])
        perm_tests(full, "réel S1-S6")
        perm_tests(secs[:5], "réel S1-S5 (sensibilité : sans la page 2 pâle)")
        anagram_test(words, "réel", words)
