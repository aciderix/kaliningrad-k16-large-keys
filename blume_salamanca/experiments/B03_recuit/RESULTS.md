# B03 — Résultats

## B03a — Clé unique (K1 = K2), w = 11 à 30 : rien
GitHub Actions, run 37190661063 (20 machines, une largeur chacune), 1000 recuits × 1 M d'itérations par largeur,
note = quadrigrammes espagnols des deux clairs complets. Sorties : `logs/B03a/shard-*.out`.

| w | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| z max | 5,4 | 5,6 | 6,4 | 6,8 | 6,8 | 7,3 | 7,3 | 7,1 | 7,6 | 7,4 | 7,9 | 7,9 | 8,3 | 8,4 | 8,4 | 8,5 | 8,6 | 8,9 | 9,4 | 9,6 |

Meilleure note de clair −13,52 (w = 30) ; une vraie clé donne z ≈ 25 et une note ≈ −9,5. Le maximum croît
régulièrement avec w : c'est le plafond du bruit, pas un signal. **Aucun candidat (seuil z ≥ 12).**
Couverture (taux de succès par recuit mesurés sur plantés à 300 k itérations : w = 15 : 1/4 ; 18 : 8/30 ;
19 : 1/50 ; 20 : 0/50) : quasi certaine jusqu'à w = 18, bonne pour w = 19 (1000 recuits plus longs), partielle
pour w = 20–21, faible au-delà.
