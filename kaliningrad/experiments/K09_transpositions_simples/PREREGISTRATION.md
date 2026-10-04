# K09 — Barrière (rail fence) et décimation, recherche exhaustive — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul (2026-09-29).

## Pourquoi
Procédés manuels simples, fréquents chez des écoliers, absents du catalogue K06 sous leur forme exacte : **barrière** à r rails
(le clair écrit en zigzag sur r lignes, lu ligne par ligne ; décalage de départ o = 0..2r−3) et **décimation** (lecture d'une lettre
toutes les k, en boucle : P[i] = C[(a + i·k) mod n], k premier avec n, départ a quelconque — équivalent : a = 0 suffit à rotation
près, on garde a = 0 et on lit le résultat comme un cercle).

## Suites
Texte entier (979 lettres) et chaque bloc S1..S6. Barrière : r = 2..min(100, n/2), chiffrement et déchiffrement (les deux sens).
Décimation : tous les k de 2 à n−1 premiers avec n. Chaque candidat aussi lu à l'envers.

## Scores
(1) quadrigrammes allemands (lettres intactes) : toutes les suites ; (2) MI(1) (substitution quelconque) : texte entier seulement
(sans puissance sur les blocs, K07).

## Contrôles
Pour chaque procédé et chaque taille (169 et 979) : 10 textes allemands réservés (sous substitution pour le score MI), paramètres
tirés au hasard ; exigé : le bon candidat classé premier ≥ 9 fois sur 10.
Nuls : 100 permutations aléatoires de chaque suite, même recherche. Décision : dépasser tous les nuls et atteindre un niveau de
langue (quadrigrammes ≥ −10,5 ; MI ≥ 0,7) ; revendication seulement sur texte lisible.

## Amendement 1 (avant le texte réel)
Critère de succès des contrôles : ≥ 90 % des lettres voisines recollées, sens et rotation indifférents (une décimation par k et par
n − k donnent le même texte lu à l'envers et décalé ; le critère « texte identique » comptait ces cas comme échecs).
