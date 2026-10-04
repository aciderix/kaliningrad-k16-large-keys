# K23 — Le reste d'ordre local vient-il d'un message ou de l'habillage ? (2026-10-03)

Statut : exploration ; la prédiction (« un message brassé avant l'habillage donne un signal des deux côtés des
espaces ») a été énoncée avant le calcul. Outils : `tools/k23/` ; sorties : `logs/results.out`.

## Idée
K19–K21 ont trouvé un reste d'ordre « allemand » entre lettres proches, interprété comme la trace d'un message brassé
localement. Autre explication : en découpant le flux en « mots » prononçables (K10–K11), l'auteur a pu aussi arranger
quelques lettres **à l'intérieur des mots**. Les deux hypothèses se séparent : un message brassé **avant** la mise en
mots laisse le signal aussi bien dans les mots qu'à cheval sur deux mots, puisque les espaces ignorent le message ;
un arrangement fait **pendant** l'habillage le concentre dans les mots.

## Mesure
Score de bigrammes allemands symétrique sur les paires à distance ≤ 4, séparé selon que les deux lettres sont dans le
même « mot » de la bouteille ou non. Témoin : la bouteille mélangée puis **redécoupée par la même règle** (probabilités
de coupure mesurées sur la bouteille selon la classe voyelle/consonne des deux lettres et la longueur du mot en cours),
ce qui neutralise l'effet mécanique de la règle (un témoin naïf donne +4,1 / −2,7 par ce seul effet).

| | dans un mot | entre deux mots |
|---|---:|---:|
| **bouteille** | **+3,0** | **+0,1** |
| allemand brassé (déplacements ≤ 50), redécoupé (4 textes) | +0,4 à +2,1 | +0,9 à +1,9 |
| allemand brassé (≤ 25) | +1,3 à +3,6 | +0,8 à +1,6 |
| allemand mélangé par paquets de 50 | −0,5 à +2,3 | +0,4 à +2,1 |

## Lecture
Dans les contrôles, le signal se répartit des deux côtés. Dans la bouteille, il est **entièrement à l'intérieur des
mots** et **absent entre les mots**. Ce n'est pas la signature d'un message allemand brassé puis habillé ; c'est celle
d'un arrangement des lettres **au moment de fabriquer les mots** (choisir ou réordonner les lettres d'un « mot » pour
qu'il ait l'air allemand). Le reste d'ordre de K19–K21 est donc probablement un **produit de l'habillage**, et non la
trace d'un clair. Cela affaiblit l'hypothèse « message allemand brassé localement » et renforce les deux autres :
flux chiffré dont l'auteur a retouché les mots, ou pseudo-texte sans message.

Réserves : un seul test, quatre contrôles par cas, dispersion importante ; à confirmer par d'autres mesures (par
exemple la position des paires dans le mot, ou des mots de longueurs différentes).

## Complément : toutes les distances (`habsig4.py`)

| distances | dans un mot | entre deux mots |
|---|---:|---:|
| 1–4 | +3,0 | +0,2 |
| 5–10 | +0,9 | +1,7 |
| 11–20 | +1,1 | +0,7 |
| 21–40 | — | +1,5 |

Paires c–h/k à ±10 : excès dans le même mot (8 contre 4,4 ; z = +1,8) et entre mots (17 contre 12,8 ; z = +1,2).
Paires voisines selon la position dans le mot : début +1,2, milieu +1,5, fin −0,3.

Lecture corrigée : le signal **à très courte distance** (1–4) vient entièrement des mots de l'habillage ; il reste
**entre les mots**, aux distances 5–40, un signal faible (≈ 2 écarts-types en combinant les bandes, qui ne sont pas
indépendantes). L'habillage explique donc la plus grande partie du « reste d'ordre » de K19, mais pas forcément tout :
un faible ordre local du flux d'origine (échelle ≈ 5–40) reste possible, à un niveau qui ne permet aucune lecture.

## Complément 2 : le flux d'origine, mots mis de côté (`cross_abc.py`)

Mesure unique fixée avant calcul : score des paires **entre deux mots**, distances 5–40, contre 2 000 témoins
redécoupés : **z = +2,2 (p ≈ 0,016)**. Estimation de l'échelle (ABC) sur ces seules paires : les échelles 31–60
sont les plus compatibles (7,9 % des simulations dans la zone retenue), mais le **mélange de tout le texte reste
presque aussi compatible (3,0 %)**, soit un rapport d'environ 2,6 seulement (contre « jamais compatible » quand les
paires internes aux mots étaient comptées, K21).

## Conclusion révisée de K19–K23

Une fois retiré l'effet de la fabrication des mots, le flux d'origine ne garde qu'une **trace faible et incertaine**
d'ordre local (p ≈ 0,02 ; un mélange complet n'est que 2 à 3 fois moins vraisemblable). L'essentiel du « reste
d'ordre » venait de l'habillage. Le portrait redevient celui de K18 : un flux de lettres sans structure exploitable,
mis en forme de « mots » par une main qui en soignait l'aspect allemand ; message chiffré (transposition non
identifiée) ou pseudo-texte, sans moyen de trancher par les fréquences.
