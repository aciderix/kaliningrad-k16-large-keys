"""K29 — suggestions externes portant sur le décompte des lettres (2A, 2B, 2C, 5).
Statistique : G = 2 Σ O ln(O/E) sur 26 lettres (accents repliés), E = profil du modèle × 979 ; référence : fenêtres
de 979 lettres de textes allemands (corpus K18), transformées par le modèle testé. p = part des fenêtres du modèle
au moins aussi éloignées que la bouteille. Modèles :
  base      : allemand transposé (K17) ;
  ê→a       : ê de la bouteille lu comme ä (replié en a, comme dans le corpus) ;
  sch→w     : le scripteur écrit « sch » avec un w (ш cursif) ;
  nombres   : mélange allemand + proportion α de nombres écrits en toutes lettres (trois genres), α ajusté ;
  séparateur: w = séparateur de mots ou de phrases (compte attendu).
Usage : K18_CORPUS=<dossier> python3 tools/k29/decompte.py"""
import sys, os, random, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'k18'))
from dewin import *
AL = 'abcdefghijklmnopqrstuvwxyz'
rnd = random.Random(29)
L = lines_v1()
rich = tokens(' '.join(L[:25]), 'rich')
def fold(sym): return unicodedata.normalize('NFKD', sym[0]).encode('ascii', 'ignore').decode()
bottle = Counter(fold(s) for s in rich)
assert sum(bottle.values()) == 979
bottle_ea = Counter(bottle); n_e_hat = sum(1 for s in rich if s[0] == 'ê'); bottle_ea['e'] -= n_e_hat; bottle_ea['a'] += n_e_hat
KEEP = ('g2229', 'g35312', 'g50285', 'g22367', 'g2407', 'g5323', 'g6498', 'g2403', 'g12108', 'g7205', 'heldout')
texts = {k: v for k, v in german_corpus().items() if any(x in k for x in KEEP)}   # corpus « propre » de K18 (K18_CLEAN)
raw = {}
for f in sorted(glob.glob(CORP + '/g*.txt')):
    if not any(x in f for x in KEEP): continue
    s = gut_body(open(f, encoding='utf-8', errors='ignore').read()).lower().replace('ß', 'ss')
    raw[f] = ''.join(c for c in unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode() if c.isalpha() and c < '{')
def G(obs, prof):
    return 2 * sum(o * math.log(o / (979 * prof[c])) for c, o in obs.items() if o > 0)
def profile(counters):
    tot = Counter()
    for c in counters: tot.update(c)
    n = sum(tot.values()); return {c: max(tot[c], 0.5) / n for c in AL}
def test(name, wins, obs):
    prof = profile(wins); g0 = G(obs, prof); gs = [G(w, prof) for w in wins]
    p = sum(g >= g0 for g in gs) / len(gs)
    print('%-44s G bouteille %7.1f | fenêtres : médiane %5.1f, max %6.1f | p = %.4f (%d fenêtres)' % (name, g0, sorted(gs)[len(gs) // 2], max(gs), p, len(gs)))
    return p
wins = [Counter(w) for k, w in windows(texts, 979, 979)]
print('== base et ê')
test('base (K17 : ê→e)', wins, bottle)
test('ê lu comme ä (→ a)', wins, bottle_ea)
print('\n== 2C : sch écrit w (ш cursif)')
wins_sch = [Counter(w) for k, w in windows({k: t.replace('sch', 'w') for k, t in raw.items()}, 979, 979)]
test('sch→w', wins_sch, bottle)
test('sch→w, et ê→ä', wins_sch, bottle_ea)
sch_rate = sum(t.count('sch') for t in raw.values()) / sum(len(t) for t in raw.values()) * 979
print('   sch par 979 lettres en allemand : %.1f (excès de w à expliquer : ≈ 20 ; déficit de c : ≈ 15)' % sch_rate)
print('\n== 2B : nombres en toutes lettres')
U = ['null', 'eins', 'zwei', 'drei', 'vier', 'fuenf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'elf', 'zwoelf']
TEEN = {13: 'dreizehn', 14: 'vierzehn', 15: 'fuenfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn'}
TENS = {2: 'zwanzig', 3: 'dreissig', 4: 'vierzig', 5: 'fuenfzig', 6: 'sechzig', 7: 'siebzig', 8: 'achtzig', 9: 'neunzig'}
def card(n):
    if n < 13: return U[n]
    if n < 20: return TEEN[n]
    if n < 100:
        t, u = divmod(n, 10); return TENS[t] if u == 0 else ('ein' if u == 1 else U[u]) + 'und' + TENS[t]
    h, r = divmod(n, 100); return ('ein' if h == 1 else U[h]) + 'hundert' + (card(r) if r else '')
def fold_txt(s): return s.replace('ue', 'u').replace('oe', 'o')      # fünf → funf (accents repliés comme le corpus)
genres = {
    'cardinaux 1–100': lambda: card(rnd.randint(1, 100)),
    'chiffres à la militaire (eins zwo … null)': lambda: ['null', 'eins', 'zwo', 'drei', 'vier', 'fuenf', 'sechs', 'sieben', 'acht', 'neun'][rnd.randrange(10)],
    'années 1900–1999 et dates': lambda: rnd.choice(['neunzehnhundert' + card(rnd.randint(1, 99)), card(rnd.randint(1, 31)) + 'ter', card(rnd.randint(1, 12))]),
}
for gname, gen in genres.items():
    numtxt = fold_txt(''.join(gen() for _ in range(40000)))
    best = None
    for alpha in [0.0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]:
        m = int(round(alpha * 979)); ws = []
        for k, w in windows(texts, 979 - m, 979):
            o = rnd.randrange(len(numtxt) - m); ws.append(Counter(w) + Counter(numtxt[o:o + m]))
            if len(ws) >= 3000: break
        prof = profile(ws); g0 = G(bottle, prof); gs = [G(w, prof) for w in ws]; p = sum(g >= g0 for g in gs) / len(gs)
        if best is None or p > best[0] or (p == best[0] and g0 < best[2]): best = (p, alpha, g0)
    nc = Counter(numtxt); tot = len(numtxt)
    print('%-44s meilleur α = %.2f : G %.1f, p = %.4f | f %.1f %% w %.1f %% n %.1f %% g %.1f %% a %.1f %% dans les nombres'
          % (gname, best[1], best[2], best[0], 100 * nc['f'] / tot, 100 * nc['w'] / tot, 100 * nc['n'] / tot, 100 * nc['g'] / tot, 100 * nc['a'] / tot))
print('\n== 2A : w = séparateur')
ref = gut_body(open(CORP + '/g22367.txt', encoding='utf-8', errors='ignore').read()).lower()   # Kafka, avec espaces
words = re.findall(r'[a-zäöüß]+', ref); letters = sum(len(w) for w in words)
sent = len(re.findall(r'[.!?]', ref))
print('   Kafka (Gutenberg 22367) : %.1f mots et %.1f phrases par 979 lettres ; w attendu ≈ 16 ; bouteille w = 36' % (979 * len(words) / letters, 979 * sent / letters))
print('   w séparateur de mots ⇒ w ≈ %.0f (incompatible) ; séparateur de phrases ⇒ w ≈ %.0f' % (16 + 979 * len(words) / letters, 16 + 979 * sent / letters))
