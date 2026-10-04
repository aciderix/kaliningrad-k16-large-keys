# K15 — RÉSULTATS (2026-09-29) : pas de chiffrement **par blocs à clé commune** (routes, colonnes, Übchi, grille tournante)

Pré-inscription : `PREREGISTRATION.md` (commit 9b4942a) + amendement 1 (effort relevé d'après les contrôles, avant le réel des
familles C, U, D, F ; ordre d'exécution : réel d'abord, nuls seulement si le seuil de langue est atteint). Outils :
`tools/k15_blocs.c`, `tools/k15_routes.py`. Sorties : `logs/`.

## 1. Contrôles (10 textes allemands en blocs de mêmes tailles, clé commune aléatoire ; succès = ≥ 90 % des voisines recollées)
| Famille | quadrigrammes (lettres intactes) | MI additionné (substitution admise) |
|---|---|---|
| R routes (même route, même largeur pour tous les blocs) | **10/10** | **10/10** |
| C colonnes à clé 5-20 | **10/10** (effort relevé ; 7/10 d'abord) | 5/10 — sans puissance |
| U même clé deux fois 5-15 | **9/10** | **7/10** |
| F grille tournante 13×13 (S2, S4, S5) | **10/10** | **8/10** |
| D double transposition par bloc 5-13 | 4/10 (effort faible), puis **6/10** (6 × 40 000) — sans puissance | 4/10 (6 × 40 000) — sans puissance |

## 2. Bouteille
| Combinaison | score réel | seuil de langue | verdict |
|---|---|---|---|
| R, MI additionné | 0,363 (nuls : moyenne 0,365, max 0,398 ; p = 0,52) | 0,7 | négatif |
| R, quadrigrammes | −14,94 (nuls : max −14,85 ; p = 0,08) | −10,5 | négatif |
| C, quadrigrammes | −14,42 | −10,5 | négatif (seuil non atteint) |
| U, quadrigrammes | −14,53 | −10,5 | négatif |
| U, MI additionné | 0,413 | 0,7 | négatif |
| F, quadrigrammes | −13,17 | −10,5 | négatif |
| F, MI additionné | **0,840** | 0,7 | seuil atteint ⇒ nuls : **0,835 à 0,867 (12 nuls, 9 ≥ réel)** ⇒ **négatif** : la recherche (4^43 clés pour 504 lettres) fabrique ce niveau de MI à partir de n'importe quelles lettres |
Nuls F-MI arrêtés à 12 sur 30 prévus (décision acquise : 9 déjà ≥ réel).

## 3. Conclusion (RÉSULTAT)
Sous l'hypothèse d'une **clé commune aux blocs**, ni une route classique (± substitution), ni une transposition en colonnes à clé
(5-20, lettres intactes), ni la même clé appliquée deux fois (5-15, ± substitution), ni une grille tournante 13×13 (± substitution)
ne produisent le flux. Non testés faute de puissance : colonnes par bloc avec substitution, double transposition par bloc à deux clés.
Leçon de méthode : un score de langue élevé (F-MI 0,84, au-dessus du seuil fixé) peut n'être qu'un artefact d'une recherche trop
libre ; seul le nul l'a montré.

## 4. Exploration déclarée (non interprétable) : double transposition par bloc, clés communes
Contrôles insuffisants (6/10 et 4/10), mais les échecs du score quadrigrammes sont souvent des détections partielles (−11,5 à −12,2,
contre ≈ −14,5 au hasard) : une bouteille ainsi chiffrée donnerait probablement un signal visible. Texte réel (quadrigrammes, 6 ×
40 000) : **−14,39** (w = 13, 13), niveau du hasard, texte illisible. Aucun indice en faveur de cette famille ; pas d'exclusion formelle.
