"""K27 — clés supplémentaires : prénoms russes et allemands, noms propres, et expressions de deux mots thématiques.
Usage : python3 tools/k27/keys_extra.py sortie.txt   (même format que keys.py)"""
import sys, itertools
sys.argv += []
exec(open('tools/k27/keys.py').read().split('def main():')[0])
RU_NAMES = '''александр алексей анатолий андрей антон аркадий артём борис вадим валентин валерий василий виктор виталий
владимир владислав вячеслав геннадий георгий григорий даниил денис дмитрий евгений егор иван игорь илья кирилл
константин леонид максим михаил никита николай олег павел пётр роман руслан сергей станислав степан тимур фёдор юрий
яков саша саня серёжа серёга вова володя дима митя женя коля миша петя паша витя толя костя лёша гоша юра слава
александра алла анастасия анна антонина валентина валерия вера галина дарья екатерина елена елизавета жанна зинаида
зоя ирина катя катерина лариса лена любовь людмила марина мария надежда наталья наташа нина оксана ольга оля полина
светлана света софья таисия тамара татьяна таня юлия юля яна маша даша настя'''.split()
DE_NAMES = '''hans peter klaus jürgen wolfgang michael thomas andreas stefan frank uwe dieter günter horst helmut heinz
werner manfred gerhard karl kurt walter fritz otto hermann wilhelm friedrich heinrich ernst paul erich herbert rudolf
anna maria ursula monika petra sabine renate karin brigitte helga gisela ingrid elke heike andrea gabriele christa
erika hildegard gertrud elisabeth margarete irmgard johanna käthe frieda luise martha'''.split()
PROPER = '''пиллау балтийск калининград кенигсберг гданьск клайпеда рига таллин ленинград москва советский балтийскфлот
балтийскоеморе куршскаякоса янтарь янтарный германия германиядр гдр фрг'''.split()
THEME = [w for w in THEME_DE if len(w) <= 10] + ['ostpreussen', 'heimat', 'liebe', 'mein', 'meine', 'unsere', 'die', 'der', 'das']
THEME_RU2 = [w for w in THEME_RU if len(w) <= 9] + ['моя', 'наша', 'мой', 'наш']
rows = []; seen = set()
def add(lab, seq):
    if not 4 <= len(seq) <= 24: return
    r = tuple(ranks(seq)); k = (len(r), r)
    if k in seen: return
    seen.add(k); rows.append((lab, r))
for w in RU_NAMES + PROPER:
    add('ru:' + w, [CYR.index(c) for c in w]); t = ''.join(TR[c] for c in w); add('rl:' + t, t)
for w in DE_NAMES:
    for x in de_variants(w): add('de:' + x, x)
for a, b in itertools.product(THEME, THEME):
    if a != b:
        for x in de_variants(a + b): add('de:' + x, x)
for a, b in itertools.product(THEME_RU2, THEME_RU2):
    if a != b:
        w = a + b; add('ru:' + w, [CYR.index(c) for c in w]); t = ''.join(TR[c] for c in w); add('rl:' + t, t)
with open(sys.argv[1], 'w', encoding='utf-8') as f:
    for lab, r in rows: f.write('%s\t%d %s\n' % (lab, len(r), ' '.join(map(str, r))))
print(len(rows), 'clés', file=sys.stderr)
