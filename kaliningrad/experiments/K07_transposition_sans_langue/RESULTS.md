# K07 — RÉSULTATS (2026-09-29) : même en admettant une **substitution** en plus, aucune route ni transposition en colonnes du texte entier

Pré-inscription : `PREREGISTRATION.md` (commit 8a1a9e4) + amendement 1 (avant le réel des familles 2-3). Outils :
`tools/k07_routes_mi.py`, `tools/k07_columnar_mi.c`. Sorties : `logs/`.
Score : information mutuelle entre lettres voisines MI(1), **invariante par toute substitution simple et toute langue**.

## 1. Contrôles (allemand réservé sous substitution aléatoire, puis transposition)
| Famille | Taille | Succès | Verdict |
|---|---|---|---|
| 1 routes | 169 / 144 | 4/10 / 4/10 | **sans puissance** sur les blocs (MI trop bruité sur ~160 lettres) |
| 1 routes | 979 | 8/10 (les 2 échecs : grilles de 2 lignes, route voisine presque équivalente) | puissant |
| 2 grille carrée à clé | 169 / 144 | 4/10 / 4/10 (recuit) | **sans puissance** |
| 3 colonnes à clé, w = 5..20 | 979 | **10/10** (tirages aléatoires) ; cas difficiles V1 à 16-20 colonnes : 3/6 retrouvés en entier, mais les échecs recollent 70-80 % des contacts avec MI = 0,73-0,83, **très au-dessus des nuls** (≈ 0,44) ⇒ détection assurée | puissant |
Valeur de référence : un allemand remis en ordre (substitué ou non) a MI ≈ 0,9-1,1.

## 2. Texte réel (979 lettres)
| Famille | MI réel | nuls | p |
|---|---|---|---|
| 1 routes (catalogue de 27 328 lectures) | 0,376 | 100 nuls : moyenne 0,370, max 0,399 | 0,19 |
| 3 colonnes à clé (w = 5..20, 2 sens, recuit) | 0,441 | 8 nuls (arrêt anticipé : 4 déjà ≥ réel, décision acquise) : moyenne 0,442, max 0,455 | 0,56 |
Blocs (familles 1-2) : rapportés dans `logs/routes_reel.out`, non interprétables (sans puissance).

## 3. Conclusion (RÉSULTAT)
Sur le texte entier, **ni une route classique, ni une transposition en colonnes à clé (5 à 20 colonnes), même suivie ou précédée
d'une substitution simple quelconque, et dans n'importe quelle langue**, ne rend au texte des contacts de langue naturelle : le
meilleur MI trouvé (0,44) est celui que la même recherche obtient sur des lettres mélangées au hasard, loin de 0,9-1,1.
Cela ferme l'hypothèse C pour ces deux familles, sans aucune hypothèse de langue.

## 4. Extension aux clés longues (amendement 2 : w = 21..40, texte entier)
Réel : MI = **0,489** (w = 35). Nuls (11 calculés avant arrêt, décision acquise) : 0,485 à 0,502, moyenne 0,495 ; 9 sur 11 ≥ réel
(p ≈ 0,8). Seuil de langue pré-inscrit (≥ 0,6) non atteint. ⇒ **pas de transposition en colonnes à clé de 21 à 40 colonnes non
plus**, avec ou sans substitution. Au total : clés de 5 à 40 colonnes exclues sur le texte entier.
