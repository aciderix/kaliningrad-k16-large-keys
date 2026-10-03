# K17 — tests invariants par transposition (2026-09-30)

Statut : exploration a posteriori (non pré-inscrite), mais à contrôle intrinsèque : la distribution de référence est
celle des fenêtres de 979 lettres de textes allemands réels, c'est-à-dire exactement ce que donnerait un vrai clair
allemand après n'importe quelle transposition. Outil : `tools/k17_profil.py` (≈ 1 s). Sortie : `logs/depot.out`.

## Principe

Une transposition — simple, double (K08, K14, K16), grille, route, nihiliste, quelle que soit la largeur ou la clé —
change l'ordre des lettres, jamais leur nombre. Avant de chercher une clé, il suffit donc de vérifier que le décompte
des 979 lettres est celui d'un texte allemand. Si ce n'est pas le cas, aucune clé ne peut produire de l'allemand, et
la recherche est inutile quelle que soit sa puissance.

## Résultats

Références : `data/heldout/de.txt` (Kafka) + `data/controle_de_kant_6343.txt` (505 fenêtres, pas de 244), puis avec
en plus Gutenberg 2229 (Goethe, *Faust I*), 35312 (Eichendorff, *Taugenichts*), 50285 (N. Jacques, *Dr. Mabuse*)
(3 259 fenêtres ; ces textes ne sont pas versés au dépôt : `python3 tools/k17_profil.py <dossier>`).

| Test | Flux | Fenêtres allemandes aussi extrêmes | Lecture |
|---|---|---|---|
| T1 transposition seule : G du décompte | 125,7 / 122,9 | **0/505 ; 0/3 259** (max 91,9 ; 117,0) | exclue |
| T1 f + w | **82** (f 46, w 36) | max 49 ; 59 | f z = +7,6, w +4,8, n +3,9 ; a, b, c, g en défaut |
| T2 transposition + substitution : profil trié | 41,9 / 43,9 | 4/505 ; 5/3 259 (fenêtres chevauchantes) | p ≈ 0,002–0,008 : très improbable |
| T3 identité des lettres contre étiquetage aléatoire | — | 0/100 000 étiquetages aussi proches de l'allemand | les lettres sont leurs propres lettres : lettres absentes = j, q, x, y, exactement les plus rares de l'allemand |

Sensibilité : en retirant f et w du décompte, le flux reste en marge (5/829 fenêtres) ; en retirant f, w, n, il
rentre dans la distribution (25/876). L'écart est donc porté surtout par **f, w et n**, lus de la même façon par la
transcription indépendante de Corsair_nv (f 3,32 %, w 2,78 % des signes) : ce n'est pas une erreur de lecture propre à v1.

Comparaison avec 17 autres langues (Gutenberg, mêmes fenêtres ; exploration) : l'allemand est de loin la plus
proche (G = 123), toutes les autres sont bien plus loin (néerlandais 347, danois 586, suédois 770, polonais 937,
tchèque 1 431, finnois 1 820…). Aucune langue testée ne rend compte du décompte.

## Conclusion (OBSERVATION forte)

1. **Aucune transposition d'un texte allemand ordinaire** ne peut donner ce flux : c'est indépendant de la clé,
   de la largeur et du nombre de passes. Les recherches K16 (quadrigrammes allemands, lettres intactes) cherchaient
   donc une clé qui ne peut pas exister ; leurs scores ≈ −14,3, au niveau du hasard, sont ceux attendus.
2. **Pas de substitution** : l'alphabet du flux est celui de l'allemand, lettre pour lettre (T3). L'hypothèse
   C (transposition + substitution) est de plus défavorisée par T2.
3. Ce qui reste compatible avec l'ensemble K02, K04, K10–K12 et K17 : un flux écrit **avec les lettres de
   l'allemand mais pas dans ses proportions** (trop de f, w, n ; trop peu de a, b, c, g), sans liaison entre lettres
   voisines, puis habillé en mots. C'est le portrait de l'hypothèse B (pseudo-texte « à l'allemande »), ou d'un clair
   dans une orthographe non standard qui reste à identifier. Les recherches de clés longues ne sont pas la bonne
   voie tant qu'un clair compatible avec T1 n'est pas proposé.

## Complément : message caché dans l'habillage ? (exploration, `tools/k17_couches.py`, `logs/couches.out`)

Si le flux n'est pas un allemand transposé, le message pourrait être porté par la mise en forme. Séquences extraites
et notées au quadrigramme allemand (allemand réel ≈ −9 à −10 ; hasard ≈ −14 à −16) : initiales des 194 mots
(−16,0), finales (−15,3), deuxièmes lettres (−15,2), lettres des abréviations `rsfdcfrlbsncrbndszrntdnrn` (−18,4),
lettres portant une apostrophe (−18,3 ; uniquement des consonnes), mots d'une lettre `eêiiêiiiii`, lettres
soulignées `epennn`. **Aucune n'est lisible** ; aucune couche simple de l'habillage ne porte un texte allemand.

## Complément : allemand avec quelques lettres échangées ou confondues ? (exploration)

Dernière échappatoire : un clair allemand dont l'auteur aurait échangé ou confondu quelques lettres avant de le
mélanger. On cherche les échanges (puis les fusions de lettres) qui rapprochent le plus la bouteille de l'allemand,
et on applique **la même optimisation** à des fenêtres allemandes pour calibrer (sinon l'optimisation seule
fabrique de l'accord).

| Échanges optimaux | Bouteille (G) | Fenêtres allemandes aussi loin après la même optimisation |
|---|---|---|
| 0 | 123,2 | 0/300 (max 90,8) |
| 1 (c↔f) | 83,0 | 0/300 (max 66,7) |
| 2 (+ g↔w) | 65,8 | 0/300 (max 54,9) |
| 3 (+ a↔c) | 57,0 | 0/300 (max 51,1) |
| 4 (+ a↔d) | 52,6 | 0/300 (max 49,2) |

Fusions de lettres (une lettre allemande écrite avec le signe d'une autre, 1 à 4 fusions) : G ≥ 112, 0/200 fenêtres.
Échanges ou fusions de quelques lettres ne rendent donc pas un profil allemand ; une substitution complète est déjà
défavorisée par T2. Il n'existe pas de transformation lettre à lettre simple qui ramène le flux à de l'allemand,
et donc pas de flux « corrigé » sur lequel relancer utilement le solveur K16.

## Complément : seulement la partie la plus sûre ? (exploration)

Même test sur la page 1 seule (L01–L20, lue de la même façon par deux transcripteurs indépendants) et sur chacun des
six blocs, calibré sur des fenêtres allemandes de même longueur (références : dépôt + Gutenberg 2229, 35312, 50285).

| Partie | Lettres | f + w | Fenêtres allemandes avec autant de f + w | G global : fenêtres ≥ |
|---|---:|---:|---:|---:|
| Page 1 (fiable) | 786 | 64 (8,1 %) | **0** | 0,2 % |
| Page 2 (pâle) | 193 | 18 (9,3 %) | 0 | 0,2 % |
| Bloc 1 | 166 | 18 | 0,02 % | 0,1 % |
| Bloc 2 | 169 | 14 | 0,2 % | 40 % |
| Bloc 3 | 162 | 13 | 0,5 % | 37 % |
| Bloc 4 | 169 | 11 | 3,6 % | 4,5 % |
| Bloc 5 | 169 | 12 | 1,8 % | 33 % |
| Bloc 6 | 144 | 14 | 0 | 0,3 % |

L'anomalie n'est pas due aux lignes douteuses : elle est aussi forte sur la page fiable, et **chacun des six
blocs** a trop de f + w (tous sous 4 %). Les blocs 2, 3 et 5 passent le test global seulement faute de puissance
(169 lettres), pas parce qu'ils ressembleraient à l'allemand. Aucune portion du texte n'est un meilleur candidat
qu'une autre ; les transpositions par bloc ont par ailleurs déjà été testées (K03, K05, K06, K13, K15).

## Complément : russe translittéré ou dialecte ? (exploration)

Références : articles Wikipédia tirés au hasard (≈ 20–65 000 lettres par langue, API publique, 2026-09-30) ; russe
converti avec quatre translittérations (allemande avec в = w, polonaise, anglaise, française). Même statistique G que
T1 ; « fenêtres ≥ » = fenêtres de 979 lettres de la langue elle-même aussi loin que la bouteille.

| Langue | G bouteille | fenêtres ≥ | o % | a % | f+w % | e+n % |
|---|---:|---:|---:|---:|---:|---:|
| **bouteille** | | | 1,9 | 4,0 | 8,4 | 31,2 |
| allemand standard (T1) | 123 | 0 | 2,5 | 5,8 | 3,2 | 27,6 |
| luxembourgeois | 221 | 0/57 | 4,0 | 7,9 | 2,7 | 26,4 |
| palatin | 223 | 0/27 | 3,6 | 8,8 | 3,7 | 21,1 |
| allemand de Pennsylvanie | 225 | 0/91 | 4,0 | 8,1 | 3,5 | 21,9 |
| bas-allemand | 282 | 0/97 | 5,4 | 8,2 | 2,2 | 24,6 |
| frison, ripuaire, bavarois, limbourgeois, flamand | 323–384 | 0 | 5–7 | 6–14 | 2–4 | 18–28 |
| russe, translit. allemande (в = w) | 703 | 0/57 | 9,5 | 9,9 | 4,5 | 13,2 |
| russe, translit. polonaise / anglaise / française | 780–1 216 | 0 | 10–12 | 10 | 0,5–4,7 | 13–14 |
| haut-sorabe, kachoube, estonien, letton, lituanien | 696–1 189 | 0 | 4–11 | 8–16 | 0,2–5 | 13–16 |

Le russe est exclu quelle que soit la translittération : le o y fait 10–12 % des lettres, contre 1,9 % dans la
bouteille (et e + n y font 13 %, contre 31 %). Aucun dialecte allemand ou néerlandais testé ne fait mieux que
l'allemand standard ; tous ont plus de a et de o et moins de f + w que la bouteille. Le yiddish (écriture hébraïque,
translittérations multiples) et le bas-prussien / plautdietsch (pas de corpus librement disponible ici) ne sont
pas testés.
