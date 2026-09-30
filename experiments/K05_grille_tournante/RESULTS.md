# K05 — RÉSULTATS (2026-09-29) : **pas de grille tournante (Fleissner)** sur les blocs carrés

Pré-inscription : `PREREGISTRATION.md` (commit 01c9362). Outil : `tools/k05_fleissner.c` (C, recuit simulé ; effort gelé :
6 redémarrages × 100 000 itérations × 8 variantes). Sorties : `logs/`.

## 1. Contrôles (texte allemand réservé, clé et variante aléatoires ; succès = ≥ 90 % des lettres voisines recollées)
| | 144 (12×12) | 169 (13×13) |
|---|---|---|
| (a) sans bruit | **19/20** | **17/20** |
| (b) 5 % de lettres remplacées | 11/20 | 10/20 |
Puissance conforme à l'exigence (≥ 80 %) sans bruit ; **moitié moins** si ~5 % des lettres sont altérées (limite à garder en tête,
vu l'excès de f/w).

## 2. Texte réel (meilleur score contre nuls = lettres du même bloc mélangées, même recherche)
| Bloc | score réel | nuls calculés | nuls : moyenne / max | nuls ≥ réel | p |
|---|---|---|---|---|---|
| S2 | −11,909 | 35 | −11,958 / −11,580 | 12 | 0,36 |
| S4 | −11,571 | 36 | −11,660 / −11,409 | 10 | 0,30 |
| S5 | −11,290 | 36 | −11,484 / −11,102 | 4 | 0,14 |
| S6 | −11,527 | 40 | −11,601 / −11,226 | 13 | 0,34 |
**Arrêt anticipé des nuls** (35-40 sur 100 prévus, ≈ 1 h 30 de calcul restant) : la règle de décision (« dépasser les 100 nuls »)
était déjà impossible à satisfaire pour chaque bloc ; les p finaux ne peuvent pas descendre sous 0,05. Un vrai texte allemand
remis en ordre score vers −9 ; les « meilleurs » résultats réels (−11,3 à −11,9) ont une apparence d'allemand fabriquée par
la recherche (4^43 clés), identique sur les nuls.

## 3. Conclusion (RÉSULTAT)
Les blocs carrés ne sont pas de l'allemand chiffré par une grille tournante standard (lecture en lignes ou colonnes, deux sens
de rotation, clair à l'endroit ou à l'envers), du moins avec des lettres intactes à ~95 % près.
