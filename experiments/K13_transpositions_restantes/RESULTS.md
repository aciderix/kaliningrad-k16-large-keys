# K13 — RÉSULTATS (2026-09-29) : ni transposition **nihiliste**, ni **Myszkowski**, ni **AMSCO**

Pré-inscription : `PREREGISTRATION.md` (commit 8b84ffc) + amendement 1 (effort gelé d'après les contrôles, avant le réel). Outil :
`tools/k13_transpositions.c` (C, recuit simulé). Sorties : `logs/`.

## 1. Contrôles (10 textes allemands réservés par combinaison ; paramètres non fournis ; succès = ≥ 90 % des voisines recollées)
| Famille × score | Succès (effort gelé) |
|---|---|
| N nihiliste, quadrigrammes, 169 / 144 | **10/10 / 10/10** (premier passage à effort faible : 6/10, 8/10) |
| M Myszkowski (5-15), quadrigrammes | **10/10** |
| M Myszkowski, MI (sous substitution) | **10/10** (premier passage : 7/10) |
| A AMSCO (3-12, départ 1/2), quadrigrammes | **10/10** |
| A AMSCO, MI (sous substitution) | **8/10** |

## 2. Texte réel
| Suite | Famille × score | réel | nuls | seuil de langue |
|---|---|---|---|---|
| S2 / S4 / S5 / S6 | N, quadrigrammes | −13,16 / −13,15 / −12,78 / −12,93 | 8 / 8 / 5 / 10 nuls (arrêt anticipé), max −13,16 / −12,75 / −12,73 / −12,63 | −10,5 : **non atteint** |
| texte entier | M, quadrigrammes | −14,55 | 30 nuls, 2 au-dessus (p ≈ 0,10) | non atteint |
| texte entier | M, MI | 0,434 | 4 nuls (arrêt anticipé), 0,413-0,434 | 0,7 : **non atteint** |
| texte entier | A, quadrigrammes | −14,78 | 18 nuls, 5 au-dessus | non atteint |
| texte entier | A, MI | 0,419 | 50 nuls, 1 au-dessus (p = 0,039) | 0,7 : **non atteint** |
Arrêts anticipés : la règle exige à la fois de dépasser les nuls et d'atteindre le niveau de langue ; le second critère était déjà
impossible. AMSCO-MI : p = 0,039 sur 6 combinaisons testées, niveau attendu par hasard ; une vraie remise en ordre donne 0,9-1,1.
Textes obtenus illisibles.

## 3. Conclusion (RÉSULTAT)
Dans leurs portées pré-inscrites, **ni la transposition nihiliste (blocs carrés, lettres intactes), ni Myszkowski (5-15 colonnes),
ni AMSCO (3-12 colonnes)** — ces deux dernières avec ou sans substitution, en toute langue pour le score MI — ne produisent le flux.
Le recensement des transpositions manuelles historiques classiques est ainsi couvert (hors clés longues des familles doubles et
variantes hors portée).
