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

## B03b — Calibration (run 37190769521) : succès par recuit, deux clés, convention directe
Espagnol télégraphique planté (615 + 160 lettres), 2 plantés × 16 recuits × 300 k par paire (réglages de B03b).
Succès sur 32 recuits (journal : `logs/B03b_calibration_grid.out`) :

| w1 \ w2 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|
| 11 | 31 | 20 | 25 | 17 | 27 |
| 12 | 28 | 15 | 28 | 12 | 9 |
| 13 | 29 | 23 | 29 | 12 | 4 |
| 14 | 32 | 16 | 20 | 15 | 7 |
| 15 | 31 | 32 | 25 | 28 | 29 |
| 16 | 32 | 12 | 15 | 2 | 2 |
| 17 | 32 | 28 | 16 | 1 | 2 |
| 18 | 31 | 17 | 7 | 3 | 0 |
| 19 | 28 | 6 | 4 | 3 | 0 |
| 20 | 24 | 11 | 6 | 0 | 0 |
| 21 | 27 | 13 | 14 | 0 | 2 |
| 22 | 32 | 20 | 17 | 18 | 1 |
| 23 | 16 | 7 | 1 | 2 | 0 |
| 24 | 29 | 0 | 3 | 0 | 0 |
| 25 | 14 | 1 | 2 | 0 | 0 |
| 26 | 12 | 2 | 0 | 0 | 0 |
| 27 | 11 | 11 | 3 | 0 | 0 |
| 28 | 27 | 13 | 1 | 0 | 0 |
| 29 | 14 | 3 | 1 | 0 | 1 |
| 30 | 3 | 8 | 0 | 0 | 0 |

Lecture : w2 = 11 est couvert partout ; w2 = 12–13 pour w1 ≤ 22 ; w2 = 14–15 seulement pour w1 ≤ 15 (et 22).
w1 = 15 (rectangle complet) et w1 = 22 sont nettement plus faciles. Le balayage B03b (annulé faute de place dans la
file) est relancé avec 64 recuits par paire au lieu de 32 : manque ≤ 2 % là où le taux est ≥ 2/32.
