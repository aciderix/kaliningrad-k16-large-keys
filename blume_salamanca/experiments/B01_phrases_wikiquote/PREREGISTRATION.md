# B01 — K2 tirée d'une phrase espagnole ou allemande (Wikiquote) — pré-inscription (2026-10-04, avant le calcul)

## Hypothèse
Le télégramme 1 (615 lettres) est un texte espagnol chiffré par double transposition directe (lignes écrites,
colonnes lues dans l'ordre de la clé, deux fois ; convention de `dct_reloaded/tools/dct_solver.c`), dont la seconde clé
K2 est le début d'une phrase de Wikiquote espagnol ou allemand (mots entiers, ou 11 à 30 premières lettres).

## Données et méthode
- Wikiquote es (385 835 phrases) et de (218 678) → 3 447 052 + 1 949 935 clés de 11 à 30 lettres
  (`tools/wikiquote_keys_11_30.py` ; extraction : `dct_reloaded/tools/wikiquote_extract.py`).
- Modèle : quadrigrammes espagnols, 6,1 millions de lettres de 10 livres de Gutenberg (`data/models/qg_es.bin`) ;
  *La Odisea* (Gutenberg 58221) réservée aux contrôles (`data/heldout/es_58221.txt`).
- `dctsolve stream` (dct_reloaded) avec `DCT_PMI=1 DCT_ANYW=1 DCT_W1=11,30 DCT_OFFMAX=2` : IDP de chaque K2 pour
  w1 = 11 à 30, sans contrainte de pgcd.

## Contrôles (faits avant ce calcul)
Clair espagnol réservé, 615 lettres, K1 et K2 tirées de la base espagnole, vraie K2 glissée parmi 100 000 leurres :
2/2 en tête, IDP vraie 0,35 et 0,36 contre ≤ 0,18 pour le meilleur leurre (avec `DCT_OFFMAX=2` ; IDP complète :
0,44 et 0,47 contre ≤ 0,25). Le décalage nul (`DCT_OFFMAX=0`) échoue sur un rectangle incomplet : écarté.

## Critère (fixé maintenant)
- Candidat : IDP ≥ 0,28 (avec `DCT_OFFMAX=2`).
- Déchiffrement : K1 par recuit (`withk2`, quadrigrammes espagnols) donnant ≥ −10,5 par quadrigramme et un texte
  espagnol lisible, **puis le télégramme 2 (160 lettres) lisible avec les mêmes clés**.
- Sinon : K2 n'est le début d'aucune phrase de ces deux bases.
