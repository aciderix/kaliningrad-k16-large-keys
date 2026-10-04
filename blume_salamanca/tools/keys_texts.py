"""Clés-phrases tirées de textes (versets, vers, lignes) : pour chaque unité (ligne de texte ou verset), le début de
l'unité tronqué à chaque longueur de lettres dans [lo, hi] et les débuts coupés aux mots. Lettres a–z ; umlauts
allemands en ae/oe/ue, ß en ss ; accents et ñ espagnols retirés. Usage :
python3 keys_texts.py lo hi sortie.txt fichier1 [fichier2 ...]   (lignes ; '[c:v] texte' des bibles accepté)
Les livres Gutenberg (en-tête « *** START ») sont aussi découpés en phrases ; les lignes restent des unités (vers)."""
import sys, re, unicodedata
import os
lo, hi, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
TRUNC = os.environ.get('KEYS_TRUNC', '1') != '0'   # KEYS_TRUNC=0 : coupes aux mots seulement
def norm(s):
    s = s.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    s = unicodedata.normalize('NFD', s); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s
PERFILE = os.environ.get('KEYS_DEDUP') == 'file'   # dédoublonnage par fichier seulement (gros corpus, mémoire bornée)
seen = set(); n = 0
with open(out, 'w') as fo:
    for fn in sys.argv[4:]:
        if PERFILE: seen = set()
        raw = open(fn, encoding='utf-8', errors='ignore').read()
        a, b = raw.find('*** START'), raw.find('*** END')
        units = raw.splitlines()
        if a >= 0:
            body = raw[raw.find('\n', a) + 1:b if b > a else len(raw)]
            units = body.splitlines() + re.split(r'(?<=[.!?;:])\s+', re.sub(r'\s+', ' ', body))
        for line in units:
            line = re.sub(r'^\[\d+:\d+\]\s*', '', line.strip())
            if not line or line.startswith('#'): continue
            words = [re.sub('[^a-z]', '', w) for w in norm(line).split()]; words = [w for w in words if w]
            letters = ''.join(words)
            cand = set(letters[:L] for L in range(lo, min(hi, len(letters)) + 1)) if TRUNC else set()
            acc = ''
            for w in words:
                acc += w
                if len(acc) > hi: break
                if len(acc) >= lo: cand.add(acc)
            for k in cand:
                if k not in seen: seen.add(k); fo.write(k + '\n'); n += 1
print(n, 'clés')
