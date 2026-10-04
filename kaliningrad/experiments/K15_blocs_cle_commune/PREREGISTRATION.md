# K15 — Chiffrement par blocs avec **clé commune**, scores additionnés sur les 6 blocs — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul (2026-09-29).

## Idée
Les 6 blocs (lettre soulignée + point ; 166, 169, 162, 169, 169, 144 lettres) sont la seule structure indépendante de l'habillage
(K10-K11). Un auteur qui chiffre bloc par bloc réutilise normalement la même clé. Sous cette hypothèse, on **additionne** l'évidence
des 6 blocs : le score MI (invariant par substitution) retrouve la puissance du texte entier, alors qu'il était sans puissance bloc
par bloc (K07) ; et des familles jamais testées par bloc deviennent accessibles.

## Familles (même clé et mêmes paramètres pour les 6 blocs ; chaque bloc chiffré indépendamment)
- **C** : colonnes à clé, largeur w = 5..20 (lignes incomplètes admises) — par bloc, seule la largeur 13/12 avait été testée (K03).
- **U** : même clé deux fois (Übchi) par bloc, w = 5..15.
- **D** : double transposition par bloc, deux clés distinctes, w1, w2 = 5..13.
- **F** : grille tournante 13×13 commune à S2, S4, S5 (blocs de 169 lettres ; S6 = 12×12 exclu faute de grille commune).
- **R** : routes du catalogue K06 (même route, même largeur, même sens pour tous les blocs).
Scores : **MI(1) additionné** (tables de paires des 6 blocs cumulées ; substitution quelconque, toute langue) et **quadrigrammes
allemands moyens** (lettres intactes). Outils : `tools/k15_blocs.c`, `tools/k15_routes.py`.

## Contrôles (avant le texte réel)
Pour chaque famille × score : 10 textes allemands réservés découpés en blocs de mêmes tailles, chiffrés bloc par bloc avec une clé
commune aléatoire (et une substitution aléatoire pour le score MI) ; paramètres non fournis ; succès = ≥ 90 % des lettres voisines
recollées (dans chaque bloc). Exigé ≥ 7/10, sinon « sans puissance » (non interprété).
Nuls : lettres mélangées **à l'intérieur de chaque bloc**, même recherche (30 ; 100 pour R).

## Décision
Répond si le meilleur score dépasse tous les nuls et atteint un niveau de langue (MI additionné ≥ 0,7 ; quadrigrammes ≥ −10,5) ;
revendication seulement sur texte lisible.

## Amendement 1 (avant tout calcul sur le texte réel des familles C, U, D, F ; la famille R, contrôles 10/10, a déjà été jugée)
Premier passage des contrôles à effort faible : C-Q 7/10, C-MI 3/10, U-Q 6/10, U-MI 4/10, D-Q 4/10, F-Q 10/10, F-MI 8/10 ; tous les
échecs sont des échecs de recherche (score trouvé < score du vrai clair), aux grandes largeurs. Effort relevé pour C et U
(8 départs × 40 000 itérations) et contrôles refaits ; D : contrôle MI interrompu (5 essais faits, trop lent), refait avec l'effort
retenu. Effort gelé après ces contrôles.
Contrôles à effort relevé (8 × 40 000) : C-Q **10/10**, U-Q **9/10**, U-MI **7/10**, C-MI 5/10 (sans puissance ; échecs à 16-19 colonnes,
remises en ordre partielles à MI 0,62-0,80). Combinaisons retenues : C-Q, U-Q, U-MI, F-Q, F-MI (effort F : 3 × 60 000) ; R déjà jugée.
Ordre d'exécution : le texte réel d'abord ; les nuls seulement si le seuil de langue est atteint (la règle exige les deux).
