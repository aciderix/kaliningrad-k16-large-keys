# K08 — RÉSULTATS (2026-09-29) : **pas de double transposition à clés courtes (3-9 colonnes)**, même avec substitution

Pré-inscription : `PREREGISTRATION.md` (commit e5c1961). Outil : `tools/k08_double_mi.c` (C, recuit simulé sur les deux clés,
score MI(1) invariant par substitution). Sorties : `logs/`.

## 1. Contrôles (allemand réservé sous substitution aléatoire, double transposition w1, w2 ∈ 3..9, largeurs non fournies)
**8/10** retrouvés en entier (≥ 90 % des voisines recollées) ; un 9e détecté mais partiel (788/978, MI = 0,83) ; un échec (MI 0,48).
Essais préalables déclarés : largeurs connues 5-9 : 11/11 ; 10-20 colonnes : 0/9 ⇒ portée limitée aux clés courtes.

## 2. Texte réel (979 lettres)
Meilleur MI sur les 49 paires de largeurs : **0,408** (w = 9, 7). Nuls (lettres mélangées, même recherche) : 16 calculés avant arrêt
(décision acquise : le réel était déjà sous le seuil de langue et au milieu des nuls) : 0,401 à 0,421, moyenne 0,409 ; 8 sur 16
≥ réel ⇒ **p ≈ 0,5**. Un texte remis en ordre donne 0,9-1,1.

## 3. Conclusion (RÉSULTAT)
Le texte n'est pas une double transposition en colonnes à clés de 3 à 9 colonnes, avec ou sans substitution simple, en aucune
langue. Les clés de 10 colonnes et plus restent hors de portée de cette méthode (sans puissance, déclaré avant calcul).
