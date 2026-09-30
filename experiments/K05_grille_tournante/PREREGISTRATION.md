# K05 — Grille tournante (Fleissner) section par section, allemand — PRÉ-INSCRIPTION

Rédigée et commitée avant toute recherche sur le texte (2026-09-29).

## Motivation
K02-K04 : lettres mélangées sur de grands blocs, espaces posés après coup ; fréquences les plus proches de l'allemand (K04 annexe :
seule langue compatible parmi 13). Tailles de sections : 169 = 13², 144 = 12² = tailles exactes de grilles tournantes (13×13
avec case centrale, 12×12), procédé allemand classique. La grille carrée à clé simple est déjà exclue (K03).

## Modèle
Section = carré q×q lu ligne par ligne (S2, S4, S5 : q = 13 ; S6 : q = 12). Clé : pour chaque orbite de 4 cases sous la rotation
d'un quart de tour, le quart de tour où elle est trouée (4 choix), plus, pour q = 13, la passe où la case centrale est lue.
Clair = passes 1 à 4 à la suite ; dans chaque passe, cases trouées en ordre de lecture. Variantes : sens de rotation (horaire /
antihoraire), lecture du carré en lignes ou en colonnes, clair à l'endroit ou à l'envers (8 variantes ; on garde la meilleure,
même règle pour contrôles et nuls). Espace des clés : 4^36 ≈ 5·10^21 (q = 12), 4^43 (q = 13).

## Recherche et score
Recuit simulé sur la clé (changement d'une orbite), score = quadrigrammes allemands (`dagapeyeff/data/models/qg_de.bin`), outil
`tools/k05_fleissner.c`. Effort fixé sur les contrôles puis gelé.

## Contrôles (avant le texte)
(a) 20 blocs de 144 et 20 de 169 lettres du texte allemand réservé, clé et variante aléatoires ; succès = ≥ 90 % des lettres
voisines recollées ; exigé ≥ 80 % de succès par taille, sinon test déclaré sans puissance (et effort augmenté si le calcul le permet).
(b) mêmes blocs avec 5 % de lettres remplacées (rapporté).
(c) nuls : 100 permutations aléatoires des lettres de chaque section réelle, même recherche.

## Décision
Une section répond si son score dépasse ses 100 nuls (p < 0,01) ; tout résultat est imprimé. Revendication seulement si le texte
obtenu est de l'allemand lisible (oracle : lisibilité, cohérence entre sections).

## Portée
Un négatif exclut la grille tournante standard (lecture en lignes/colonnes) sur ces sections ; il laisse les routes spirales,
doubles transpositions, grilles à trous non standard, et B (pseudo-texte).
