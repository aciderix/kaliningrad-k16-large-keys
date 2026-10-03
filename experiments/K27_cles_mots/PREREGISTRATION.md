# K27 — Double transposition à clés-mots : pré-inscription (2026-10-03, rédigée pendant le calcul sur la bouteille, avant d'en voir le résultat)

## Hypothèse testée
Le flux de 979 lettres est un clair allemand (avec ou sans ≈ 10 % de nuls f/w/n, cf. K18) chiffré par une
**double transposition en colonnes** (incomplète, écrite en lignes, colonnes lues dans l'ordre de la clé) dont les
deux clés sont des **mots** : mot allemand, ou mot russe numéroté dans l'ordre de l'alphabet cyrillique, ou mot russe
translittéré numéroté dans l'ordre latin. Même clé deux fois (Übchi) comprise. Texte entier, et chaque bloc
(166, 169, 162, 169, 169, 144) chiffré séparément avec la même paire.

K08 (clés 3–9), K14 (Übchi 10–15) et K16 (recuit, clés 10–20, puissance 3/10) ne couvrent pas les clés longues
quelconques ; si les clés sont des mots, une recherche **exhaustive sur un dictionnaire** a toute la puissance voulue,
quelle que soit leur longueur.

## Méthode (`tools/k27/`)
- Clés : 20 000 mots allemands et 20 000 mots russes les plus fréquents (listes FrequencyWords, sous-titres 2018) +
  ≈ 100 mots thématiques (Heimat, Pillau, Baltijsk, Königsberg, родина, Балтийск, флот, тайна…) ; longueurs 4–24 ;
  variantes ä→a / ä→ae, ß→ss ; doublons de permutation éliminés : **28 380 clés distinctes**, soit
  8,05 × 10⁸ paires ordonnées.
- Variantes de lecture : chaque étape avec l'ordre de la clé à l'endroit ou à l'envers (4 combinaisons) ;
  extension prévue : chaque étape aussi dans le sens inverse (écrire en colonnes, lire en lignes ; 16 combinaisons).
- Note : quadrigrammes allemands (`data/models/qg_de.bin`), criblage sur les 120 premières lettres (seuil −12,8 par
  quadrigramme), puis note sur le texte entier.

## Contrôles (avant la bouteille)
Allemand réservé (Kafka) + 99 nuls f/w/n placés au hasard, chiffré avec deux clés tirées du dictionnaire réduit
(2 682 clés) : 5/5 retrouvés en tête (texte entier 3/3, par bloc 2/2), note −10,9 à −11,3 contre au plus −12,8 pour
les autres paires au criblage.

## Critère de décision (fixé avant le calcul)
- **Déchiffrement** si une paire donne une note complète ≥ −12,0 **et** un texte lisible en allemand sur l'ensemble.
- Sinon, l'hypothèse « double transposition à clés-mots de ce dictionnaire » est **exclue** (puissance des contrôles
  5/5) ; les clés hors dictionnaire (mots rares, noms propres, phrases, clés numériques) restent non couvertes.
