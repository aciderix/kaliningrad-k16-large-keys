# K03 — RÉSULTATS (2026-09-28) : **pas de grille carrée à clé** sur un texte allemand (S2, S4, S5, S6)

Pré-inscription : `PREREGISTRATION.md` (commit fe31cbf ; correction de V2 et outil, commit suivant ; amendement 1 sur le critère de
succès des contrôles, avant le texte réel). Outil : `tools/k03_columnar.c` (C). Sorties : `logs/`.

## 1. Contrôles (texte allemand réservé ; effort gelé : 100 redémarrages × 4 000 itérations × 4 lectures)
| Contrôle | 169 lettres (13×13) | 144 lettres (12×12) |
|---|---|---|
| (a) clé aléatoire, V1 ou V2 | **19/20** | **20/20** |
| (b) idem + 5 % de lettres remplacées au hasard | **20/20** | **20/20** |
Critère : ≥ 90 % des lettres voisines recollées. ⇒ test **puissant**, et robuste à une altération de l'ordre de l'écart de
fréquences observé (K02 : excès de f et w ≈ 5 % des lettres).

## 2. Texte réel (v1, variante A) — meilleur score contre 200 nuls (lettres de la même section mélangées, même recherche)
| Section | score réel | nuls : moyenne / max | nuls ≥ réel | p |
|---|---|---|---|---|
| S2 (169) | −13,48 | −13,53 / −13,03 | 78 | 0,39 |
| S4 (169) | −13,27 | −13,20 / −12,70 | 141 | 0,71 |
| S5 (169) | −12,87 | −13,10 / −12,64 | 28 | 0,14 |
| S6 (144) | −13,20 | −13,10 / −12,40 | 145 | 0,73 |
(Un vrai texte allemand déchiffré se situe vers −9,1.) Meilleurs « déchiffrements » illisibles, par exemple S5 :
`zlkewennreiniebewenluegstorartnicastrdeeweowarhens…` (sorties complètes dans `logs/reel_S*.out`).

## 3. Conclusion (RÉSULTAT)
Aucune section ne répond : **les sections carrées ne sont pas de l'allemand transposé par une grille carrée à clé simple**
(colonnes à clé ou opération inverse), lettres inchangées ou presque. La coïncidence 169 = 13², 144 = 12² n'est donc pas expliquée
par ce mécanisme. Restent ouverts (portée pré-inscrite) : routes non colonnaires, doubles transpositions, grilles tournantes,
transposition + substitution, autre langue, et l'hypothèse B (pseudo-texte).
