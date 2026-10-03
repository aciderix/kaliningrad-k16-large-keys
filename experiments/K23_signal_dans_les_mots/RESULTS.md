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
