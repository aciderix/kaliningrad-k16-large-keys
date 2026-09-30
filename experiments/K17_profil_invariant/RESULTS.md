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
