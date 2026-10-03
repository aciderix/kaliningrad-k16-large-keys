"""K27 — listes de clés-mots pour dictdt.c.
Sources : listes de fréquence FrequencyWords (H. Dave, sous-titres OpenSubtitles 2018, CC-BY-SA) :
  https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/de/de_50k.txt (idem ru)
Usage : python3 tools/k27/keys.py <dossier des listes> <nb_de> <nb_ru> <sortie>
Rangs : ordre alphabétique, ex aequo de gauche à droite. Allemand : ä→a et ä→ae (idem ö ü), ß→ss.
Russe : ordre de l'alphabet cyrillique (ё après е) ET ordre latin d'une translittération simple."""
import sys, os, unicodedata
CYR = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
TR = dict(zip(CYR, ['a','b','v','g','d','e','e','zh','z','i','i','k','l','m','n','o','p','r','s','t','u','f','kh','ts','ch','sh','shch','','y','','e','iu','ia']))
THEME_DE = '''heimat eimat pillau baltijsk baltiysk baltisk baltiisk koenigsberg konigsberg kaliningrad ostpreussen preussen ostsee
deutschland vaterland sowjetunion udssr pionier komsomol leningrad moskau moskwa lenin stalin flaschenpost geheim geheimnis
schatz freundschaft frieden krieg marine flotte schiff hafen festung leuchtturm samland memel danzig berlin wehrmacht
kriegsmarine heimatland mutter vater liebe freiheit geheimschrift schluessel botschaft nachricht'''.split()
THEME_RU = '''родина балтийск пиллау калининград кенигсберг балтика балтфлот флот тайна шифр шифровка клад пионер пионеры комсомол
ленин сталин москва мир дружба война победа письмо бутылка море маяк крепость германия ссср союз родные мама папа
свобода любовь секрет ключ послание записка гавань корабль'''.split()
def ranks(s):
    o = sorted(range(len(s)), key=lambda i: (s[i], i)); r = [0] * len(s)
    for k, i in enumerate(o): r[i] = k
    return r
def de_variants(w):
    w = w.lower().replace('ß', 'ss'); out = set()
    for mode in (0, 1):
        x = ''.join((c + 'e' if mode else c) if c in 'äöü' else c for c in w)
        x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode()
        if x.isalpha() and x.isascii(): out.add(x)
    return out
def main():
    d, nde, nru, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    seen = {}; rows = []
    def add(lab, seq):
        if not 4 <= len(seq) <= 24: return
        r = tuple(ranks(seq)); key = (len(r), r)
        if key in seen: return
        seen[key] = lab; rows.append((lab, r))
    def words(f, n):
        out = []
        for line in open(os.path.join(d, f), encoding='utf-8'):
            w = line.split()[0]
            if w.isalpha(): out.append(w)
            if len(out) >= n: break
        return out
    for w in THEME_DE:
        for x in de_variants(w): add('de:' + x, x)
    for w in THEME_RU:
        add('ru:' + w, [CYR.index(c) for c in w]); t = ''.join(TR[c] for c in w); add('rl:' + t, t)
    for w in words('de_50k.txt', nde):
        for x in de_variants(w): add('de:' + x, x)
    for w in words('ru_50k.txt', nru):
        w = w.lower()
        if all(c in CYR for c in w):
            add('ru:' + w, [CYR.index(c) for c in w]); t = ''.join(TR[c] for c in w); add('rl:' + t, t)
    with open(outp, 'w', encoding='utf-8') as f:
        for lab, r in rows: f.write('%s\t%d %s\n' % (lab, len(r), ' '.join(map(str, r))))
    print(len(rows), 'clés distinctes', file=sys.stderr)
main()
