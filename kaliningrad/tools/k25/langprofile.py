"""K25: bottle letter profile vs ~100 languages (Leipzig corpora, sentences files in $K25_TXT/<iso>.txt).
Two tests per language:
 - sorted profile (invariant under any one-to-one substitution): G of bottle vs language, p = share of 979-letter
   windows of the language at least as far; 4 readings of the bottle x 2 readings of the language (diacritics kept/folded)
 - direct counts (transposition only, Latin script): G letter by letter with diacritics folded; p from windows."""
import os, sys, glob, math, random, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'k18'))
from common import lines_v1, tokens, Counter
TXT = os.environ.get('K25_TXT', 'txt')
N = 979
fold = lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
L = lines_v1(); rich = tokens("\n".join(L[:-1]), 'rich')
bot = {'plain': Counter(fold(s).replace("'", "") for s in rich),
       'accents': Counter(s.replace("'", "") for s in rich),
       'apostr': Counter(fold(s) for s in rich),
       'all': Counter(rich)}
def letters(text, keep):
    out = []
    for ch in text.lower():
        if not ch.isalpha(): continue
        if keep: out.append(ch)
        else:
            f = fold(ch)
            if f: out.extend(f)
            elif unicodedata.category(ch).startswith('L'): out.append(unicodedata.normalize('NFD', ch)[0])
    return out
def Gsorted(counts, p):
    n = sum(counts); cs = sorted(counts, reverse=True); ps = p + [1e-5] * max(0, len(cs) - len(p))
    return 2 * sum(c * math.log(c / (n * q)) for c, q in zip(cs, ps) if c > 0)
def Gdirect(cnt, P):
    n = sum(cnt.values())
    return 2 * sum(c * math.log(c / (n * P.get(k, 1e-5))) for k, c in cnt.items() if c > 0)
rng = random.Random(1)
rows = []
for f in sorted(glob.glob(TXT + '/*.txt')):
    lang = os.path.basename(f)[:-4]
    text = open(f, encoding='utf-8', errors='ignore').read()
    res = {}
    for keep in (True, False):
        s = letters(text, keep)
        tot = len(s); ct = Counter(s)
        # drop symbols below 1e-4 (stray foreign letters) from the reference profile
        ct = Counter({k: v for k, v in ct.items() if v / tot >= 1e-4}); tot = sum(ct.values())
        p = sorted([v / tot for v in ct.values()], reverse=True)
        W = [Counter(s[i:i + N]) for i in range(0, len(s) - N, N)]
        if len(W) > 2000: W = rng.sample(W, 2000)
        gw = sorted(Gsorted(list(w.values()), p) for w in W)
        for k, c in bot.items():
            g = Gsorted(list(c.values()), p)
            res[('sort', keep, k)] = (g, sum(x >= g for x in gw) / len(gw))
        if not keep:
            P = {k: v / tot for k, v in ct.items()}
            latin = sum(v for k, v in ct.items() if 'a' <= k <= 'z') / tot
            if latin > 0.9:
                gd = [Gdirect(w, P) for w in W]
                g = Gdirect(bot['plain'], P)
                res['direct'] = (g, sum(x >= g for x in gd) / len(gd))
                res['jqxy'] = sum(P.get(x, 0) for x in 'jqxy')
    best = max((v[1], k) for k, v in res.items() if isinstance(k, tuple))
    rows.append((best[0], lang, res, best[1], len(W)))
rows.sort(key=lambda r: -r[0])
print(f"{'lang':5s} {'best p (sorted)':>15s} reading | plain-folded G,p | direct G,p | P(jqxy) | windows")
for bp, lang, res, k, nw in rows:
    pf = res[('sort', False, 'plain')]
    d = res.get('direct'); j = res.get('jqxy')
    print(f"{lang:5s} {bp:15.4f} {('kept' if k[1] else 'fold')+'/'+k[2]:14s} | {pf[0]:6.1f} {pf[1]:.4f} | "
          + (f"{d[0]:6.1f} {d[1]:.4f}" if d else '     -      -') + (f" | {j:.4f}" if j is not None else ' |   -   ') + f" | {nw}")
