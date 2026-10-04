# K09 — RÉSULTATS (2026-09-29) : ni **barrière** (rail fence) ni **décimation**

Pré-inscription : `PREREGISTRATION.md` (commit f7e4ff7) + amendement 1 (critère des contrôles, avant le réel). Outil :
`tools/k09_simples.py`. Sorties : `logs/`.

## 1. Contrôles (10 textes allemands réservés par cas ; succès = ≥ 90 % des voisines recollées)
| Taille | Procédé | quadrigrammes (lettres intactes) | MI (sous substitution) |
|---|---|---|---|
| 169 | barrière | 10/10 | 7/10 (non utilisé sur les blocs, comme prévu) |
| 169 | décimation | 10/10 | 10/10 |
| 979 | barrière | 10/10 | 10/10 |
| 979 | décimation | 10/10 | 10/10 |
Catalogue : barrière r = 2..100 × tous les décalages × 2 sens, + toutes les décimations (14 099 à 20 679 lectures).

## 2. Texte réel (meilleur score contre 100 nuls)
| Suite | quadrigrammes : réel / nuls max | p |
|---|---|---|
| S1 | −14,74 / −14,39 | 0,48 |
| S2 | −14,13 / −13,79 | 0,38 |
| S3 | −13,76 / −13,70 | 0,03 |
| S4 | −13,94 / −13,07 | 0,81 |
| S5 | −13,89 / −13,49 | 0,82 |
| S6 | −13,85 / −13,31 | 0,86 |
| texte entier | −14,95 / −14,83 | 0,28 |
| texte entier, **MI** (substitution admise) | 0,391 / 0,392 (moyenne 0,375) | 0,02 |
Niveau d'un texte remis en ordre : quadrigrammes ≈ −9 ; MI ≈ 0,9-1,1. Textes obtenus illisibles.

## 3. Conclusion (RÉSULTAT)
Aucune suite ne dépasse ses nuls ni n'approche un niveau de langue : **ni barrière (2 à 100 rails), ni décimation**, avec lettres
intactes (blocs et texte entier) ou sous substitution (texte entier).
