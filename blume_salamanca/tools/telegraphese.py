"""Texte espagnol « télégraphique » de substitution pour les contrôles plantés (BLUME).
Part d'un texte Gutenberg brut réservé (non utilisé pour le modèle), retire les accents, supprime la plupart des mots
outils (articles, que, y, de…), insère de temps en temps des nombres en toutes lettres et des mots de commerce, et
« X » comme point (usage des chiffreurs formés à l'allemande). Usage :
python3 telegraphese.py brut.txt sortie.txt [graine]"""
import sys, re, random, unicodedata
src, out = sys.argv[1], sys.argv[2]; rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
raw = open(src, encoding='utf-8', errors='ignore').read()
a, b = raw.find('*** START'), raw.find('*** END'); raw = raw[a:b] if a >= 0 and b > a else raw
raw = unicodedata.normalize('NFD', raw.lower()); raw = ''.join(ch for ch in raw if unicodedata.category(ch) != 'Mn')
sents = re.split(r'[.;:!?]+', raw)
STOP = set('el la los las un una unos unas que y de del al lo se a en por con su sus le les me mi'.split())
NUM = ('uno dos tres cuatro cinco seis siete ocho nueve diez veinte treinta cuarenta cincuenta cien ciento doscientos '
       'quinientos mil millon').split()
TRADE = ('pesetas francos precio kilos toneladas entrega pago contrato compra venta oferta importe factura cuenta banco '
         'credito mercancia envio puerto barco tren expedicion material maquinas fabrica pedido urgente confirmen '
         'telegrafien recibido conforme condiciones plazo dias semana enero febrero').split()
words = []
for s in sents:
    ws = re.findall(r'[a-z]+', s)
    if not ws: continue
    for w in ws:
        if w in STOP and rnd.random() < 0.8: continue
        words.append(w)
        if rnd.random() < 0.04: words += [rnd.choice(NUM) for _ in range(rnd.randint(1, 3))]
        if rnd.random() < 0.04: words.append(rnd.choice(TRADE))
    if rnd.random() < 0.3: words.append('x')
txt = ''.join(words)
open(out, 'w').write(txt + '\n')
from collections import Counter
c = Counter(txt); n = len(txt)
print(n, ' '.join('%s%.1f' % (k, 100 * v / n) for k, v in c.most_common(26)))
