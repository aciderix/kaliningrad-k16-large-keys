# K06 — RÉSULTATS (2026-09-29) : **aucune route classique** ne produit de l'allemand (sections et texte entier)

Pré-inscription : `PREREGISTRATION.md` (commit 038dc4c). Outil : `tools/k06_routes.py` ; sorties : `logs/`.

## 1. Contrôles (texte allemand réservé chiffré par une route et une largeur tirées au hasard)
169 lettres : **10/10** retrouvés ; 144 : **10/10** ; 984 : **9/10** (l'échec : largeur 479, grille de 2 lignes où deux spirales
donnent presque le même texte). Catalogue : 28 routes × 2 opérations (lecture / inverse) × largeurs 2..n/2 × 2 sens de lecture,
soit 4 480 à 27 496 lectures par suite.

## 2. Texte réel (meilleur score du catalogue contre 100 nuls)
| Suite | meilleure lecture | score | nuls max / moyenne | p |
|---|---|---|---|---|
| S1 (166) | w = 22, diagonales, inverse | −15,02 | −14,54 / −14,95 | 0,68 |
| S2 (169) | w = 45, colonnes | −14,45 | −13,91 / −14,36 | 0,68 |
| S3 (162) | w = 30, colonnes, inverse, envers | −13,745 | −13,746 / −14,19 | 0,010 (1 000 nuls : **0,010**, 9 nuls au-dessus) |
| S4 (169) | w = 18, spirale | −14,15 | −13,73 / −14,05 | 0,77 |
| S5 (169) | w = 9, diagonales, inverse | −13,78 | −13,66 / −14,00 | 0,11 |
| S6 (144) | w = 26, diagonales | −13,55 | −13,54 / −13,91 | 0,030 |
| texte entier (979) | w = 63, diagonales, inverse | −14,95 | −14,91 / −15,03 | 0,089 |

Un texte allemand correctement remis en ordre score vers **−9**. Meilleure lecture de S3 :
`dredthageansidnwhenftreedhnunthbzewfufiizaheredfitssdedsenimhnthrsetduwerschnunte…` (illisible).

## 3. Conclusion (RÉSULTAT)
- Aucune suite ne répond de façon crédible. S3 atteint exactement le seuil par suite (p = 0,010, confirmé avec 1 000 nuls),
  mais avec 7 suites testées le taux de fausse alarme global est ≈ 7 % ; son score reste à 4,7 points de l'allemand et son texte
  est illisible : **faux positif attendu**, noté pour transparence.
- **Les routes classiques (colonnes, zigzags, diagonales, spirales, toutes largeurs) sont exclues**, par section comme sur le texte
  entier.
