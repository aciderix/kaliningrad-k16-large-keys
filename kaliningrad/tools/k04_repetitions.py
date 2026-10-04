#!/usr/bin/env python3
"""K04 — nombre de multiensembles de lettres distincts parmi 194 mots consécutifs (voir experiments/K04_repetitions_mots/).
Usage : python3 tools/k04_repetitions.py <dossier_corpus_1> [<dossier_corpus_2> ...]
Chaque fichier <langue>_<id>.txt ou train_<langue>.txt d'un dossier est un texte de référence."""
import sys, os, re, glob, unicodedata, collections, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
NW = 194

def strip_acc(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w.lower()) if unicodedata.category(c) != 'Mn')

def words_of(text):
    """Jetons séparés par des espaces ; on garde les lettres (tous alphabets), accents fusionnés."""
    out = []
    for tok in text.split():
        w = ''.join(c for c in strip_acc(tok) if c.isalpha())
        if w: out.append(w)
    return out

def D(ws):
    return len({''.join(sorted(w)) for w in ws})

def gutenberg_body(t):
    a = t.find('*** START'); b = t.find('*** END')
    if a >= 0: t = t[t.find('\n', a) + 1:]
    if b >= 0: t = t[:t.find('*** END')] if '*** END' in t else t
    return t

def windows(ws):
    return [D(ws[i:i + NW]) for i in range(0, len(ws) - NW, NW // 2)]

if __name__ == '__main__':
    L = [l[4:].rstrip() for l in open(os.path.join(ROOT, 'data', 'transcription_v1.txt'), encoding='utf-8') if l.startswith('L')]
    cw = words_of(' '.join(L).replace('_', ''))
    dc = D(cw)
    print(f"chiffré : {len(cw)} mots, D = {dc}")
    per = collections.defaultdict(list)
    for d in sys.argv[1:]:
        for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
            b = os.path.basename(f)
            m = re.match(r'(?:train_|held_)?([a-z]{2})(?:_\d+)?\.txt$', b)
            if not m: continue
            t = gutenberg_body(open(f, encoding='utf-8', errors='ignore').read())
            ws = words_of(t)
            if len(ws) < 2 * NW: continue
            per[m.group(1)] += windows(ws)
    print("langue  fenêtres  D moyen  D max  fenêtres >= chiffré")
    allmax = 0
    for lang in sorted(per):
        v = per[lang]; allmax = max(allmax, max(v))
        print(f"{lang:6s} {len(v):8d} {sum(v)/len(v):8.1f} {max(v):6d} {sum(x >= dc for x in v):8d}")
    print(f"max toutes langues = {allmax} ; chiffré = {dc}")
    # contrôle positif : allemand transposé par grille à clé (K03, V1) puis recoupé avec les longueurs de mots du chiffré
    R = random.Random(4)
    de = [c for c in open(os.path.join(ROOT, 'data', 'controle_de_kant_6343.txt'), encoding='utf-8').read().split('\n', 1)[1].lower()
          if c in 'abcdefghijklmnopqrstuvwxyz']
    lens = [len(w) for w in cw]; n = sum(lens); vals = []
    for rep in range(20):
        o = R.randrange(len(de) - n - 200); seq = de[o:o + n + 200]; out = []
        for k in range(0, n + 169, 169):
            blk = seq[k:k + 169]
            if len(blk) < 169: break
            perm = list(range(13)); R.shuffle(perm)
            out += [blk[r * 13 + perm[j]] for j in range(13) for r in range(13)]
        out = out[:n]; ws = []; k = 0
        for l in lens: ws.append(''.join(out[k:k + l])); k += l
        vals.append(D(ws))
    print(f"contrôle positif (allemand transposé, faux mots) : D moyen {sum(vals)/len(vals):.1f}, min {min(vals)}, max {max(vals)}")
