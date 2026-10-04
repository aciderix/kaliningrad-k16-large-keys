# K08 — Double transposition en colonnes (« Würfel »), score insensible à la substitution — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul sur le texte réel (2026-09-29). Déjà fait (déclaré) : essais de faisabilité sur textes
allemands synthétiques sous substitution, largeurs **connues** : 5-9 colonnes : 11/11 retrouvés ; 10-15 et 16-20 colonnes :
0/9 (la recherche reste au niveau du hasard). Le test ne vaut donc que pour des clés courtes.

## Modèle
Clair (979 lettres, texte entier) → transposition en colonnes, clé k1 de w1 colonnes (écriture en lignes, dernière ligne
incomplète, lecture des colonnes dans l'ordre de la clé) → même opération avec k2 de w2 colonnes = chiffré. Éventuellement avec
une substitution simple en plus (le score l'ignore). **Portée : w1, w2 ∈ 3..9** (49 paires de largeurs).

## Recherche et score
Pour chaque paire (w1, w2) : recuit simulé sur (k1, k2) maximisant MI(1) du clair candidat (`tools/k08_double_mi.c`), 3 départs ×
40 000 itérations (effort fixé sur les essais ci-dessus ; augmenté seulement si les contrôles ci-dessous échouent, puis gelé).
Meilleur MI sur les 49 paires.

## Contrôles (avant le texte)
10 textes allemands réservés sous substitution aléatoire, doublement transposés avec w1, w2 tirés dans 3..9 (largeurs **non**
fournies à la recherche) ; succès = ≥ 90 % des lettres voisines recollées ; exigé ≥ 8/10.
Nuls : 100 permutations aléatoires du texte réel, même recherche.

## Décision
Le texte répond si son MI maximal dépasse ses 100 nuls et atteint un niveau de langue (≥ 0,7 ; langue remise en ordre ≈ 0,9-1,1) ;
la remise en ordre est alors attaquée comme une substitution simple. Un négatif exclut la double transposition à clés de 3 à 9
colonnes (avec ou sans substitution), pas les clés plus longues.
