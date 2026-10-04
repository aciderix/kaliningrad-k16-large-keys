# B03 — Recherche de clés aléatoires par recuit (pré-inscription)

## B03a — Clé unique (K1 = K2, type ÜBCHI), w = 11 à 30
**Méthode.** `tools/bdt.c samescan` : recuit sur la clé K (mouvements : échanges de colonnes de même longueur,
échanges, glissements, blocs, pivot, décalage d'indices), note = quadrigrammes espagnols des deux clairs complets
(T1 et T2 déchiffrés avec la même clé). 1000 recuits × 1 M d'itérations par largeur (GitHub Actions, une largeur par
machine). z = (meilleure note − moyenne de 500 clés aléatoires) / écart-type.

**Contrôles plantés** (espagnol télégraphique, 615 + 160 lettres, mêmes clés ; 300 k itérations par recuit) : taux
de succès par recuit 1/4 (w = 15), 8/30 (w = 18), 1/50 (w = 19), 0/50 (w = 20), 0/30 (w = 21). Une vraie clé donne
z ≈ 25 ; le recuit sur les vrais télégrammes (8 recuits, w = 11–16) plafonne à z = 5,3–6,5 (niveau du bruit).

**Décision.** Candidat si z ≥ 12 ; retenu seulement si les deux clairs sont de l'espagnol lisible. Couverture
attendue : quasi certaine pour w ≤ 18, partielle pour w = 19–21, faible au-delà (à dire dans les résultats).

## B03b — Deux clés, w2 = 11 à 15 (au-delà de l'exclusion de Bourdeau w2 ≤ 10)
**Méthode.** `tools/bdt.c scan` : recuit de K2 noté par l'IDP de T1 (bigrammes PMI), puis finition ; au-dessus du
seuil, recuit de K1 aux quadrigrammes sur T1 et T2. Paramètres fixés après la calibration (taux de succès par
recuit selon w1, w2), consignés ici avant le lancement.
