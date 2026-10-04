# B06 — Rectangle de K1 complet (w1 = 15) : résultats

**Passe locale** (64 recuits × 1 M d'itérations par largeur, T1 + T2, seuil z ≥ 12) : w2 = 16 : z = 6,6 ;
w2 = 17 : z = 5,4 ; w2 = 18 : z = 6,4 (bruit ; une vraie K2 donne z ≈ 20). Avec un taux de succès par recuit de
≈ 1/16 (calibration), la probabilité de manquer la vraie clé est ≈ 2 % par largeur : **w1 = 15 × w2 = 16–18 exclu**.
Journal : `logs/local_w2_16-18.out`. La passe Actions (w2 = 16–35, 256 recuits par largeur) complète au-delà.

**Passe Actions** (run 37194255505, 256 recuits × 1 M par largeur, w2 = 16–35) : z(T1) max **10,0** (w2 = 32 et 35),
croissant avec w2 comme le plafond du bruit ; aucune paire n'atteint le seuil z ≥ 12, l'étape K1 ne s'est pas
déclenchée. Avec ≈ 1/16 de succès par recuit jusqu'à w2 = 18, 256 recuits excluent ces largeurs (manque < 10⁻⁶) ;
au-delà de w2 ≈ 20 le taux par recuit est inconnu (0/16 à w2 = 20) : couverture partielle seulement.
| w2 | 16 | 17 | 18 | 19 | 20 | 22 | 25 | 28 | 30 | 32 | 35 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| z(T1) max | 5,7 | 6,0 | 5,7 | 6,9 | 7,3 | 8,4 | 8,0 | 7,9 | 8,0 | 10,0 | 10,0 |
