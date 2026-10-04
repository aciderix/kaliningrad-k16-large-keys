# Double Column Transposition Reloaded (MysteryTwister C3, 2013)

> Commandes à lancer depuis `dct_reloaded/`.

## Les cibles (vérifiées le 2026-10-04 sur mysterytwister.org : 0 solution pour chacune)

| Partie | Lettres | Clés | Clair | Solution demandée | Fichier |
|---|---:|---|---|---|---|
| 1 | 613 | 20–27, premières entre elles, **tirées de phrases anglaises** | anglais | 34 premières lettres | `data/reloaded_part1.txt` |
| 2 | 637 | 20–27, premières entre elles, aléatoires | **deux textes anglais entrelacés mot à mot** | 37 premières lettres | `data/reloaded_part2.txt` |
| 3 | 1006 | 27–34, premières entre elles, aléatoires | allemand | 48 premières lettres | `data/reloaded_part3.txt` |

Auteurs : A. Wacker, B. Esslinger, K. Schmeh (énoncés : `https://mysterytwister.org/media/challenges/pdf/mtc3-wacker-0{8,9}-DCTreloaded-0{1,2}-en.pdf`,
`…-10-DCTreloaded-03-en.pdf`). La partie 3 est aussi publiée par K. Schmeh (Cipherbrain, 25/01/2018, « Top 50
unsolved #13 ») : texte identique.

État connu (même billet, commentaire de G. Lasry, 25/01/2018) : sa recherche par recuit ne résout pas les clés
longues (> 27) ; une attaque par dictionnaire de phrases (des dizaines de milliards, Wikipédia + Gutenberg, 1 M de
clés/s sur GPU) n'a pas trouvé la clé K2 de la partie 1. Il juge les parties 2 et 3 « non solubles », la partie 1
peut-être.

## Calibration (`data/calibration/`)

| Texte | Lettres | Clés | Statut | Usage |
|---|---:|---|---|---|
| `schmeh_2007_dct_599.txt` | 599 | 21 et 23, phrases anglaises | **résolu** par G. Lasry (2013, Cryptologia 38(3), 2014) | preuve de puissance du solveur à 21×23 |
| `schmeh_2020_1_456.txt` | 456 | ≈ 10 et 11, aléatoires | résolu (« Narga », 2020) | contrôle facile |
| `schmeh_2020_2_480.txt` | 480 | 9 et 12 annoncées | les clés publiées ne déchiffrent pas : erreur de chiffrement probable | curiosité |

## Plan
1. Modèles anglais (quadrigrammes, 6-grammes) ; contrôles plantés de 600 lettres à 20–27 colonnes.
2. Reproduire la solution de 2007 (21×23) : si le solveur n'y arrive pas, il n'a aucune chance sur Reloaded.
3. Partie 1 : recuit IDP sur toutes les paires de largeurs premières entre elles 20–27, puis attaque par phrases
   pour K2.

## Cellules
| Cellule | Question | Résultat |
|---|---|---|
| [D01 étalonnage 2007](experiments/D01_calibration_2007/RESULTS.md) | notre chaîne casse-t-elle le défi de 2007 (21×23) ? | recuit aveugle : non ; **dictionnaire de phrases (IDP) : oui**, K2 = « preponderance of evidence », clair retrouvé |
| [D02 Wikiquote, partie 1](experiments/D02_wikiquote_part1/RESULTS.md) (pré-inscrit) | K2 de la partie 1 est-elle un début de phrase de Wikiquote ? | débuts en mots entiers (8,5 M) : **non** ; phrases coupées à 20–27 lettres (37 M) : en cours |

## Outils
- `tools/dct_solver.c` (dérivé de `kaliningrad/tools/k16_double_ct2.c`, IDP de CrypTool 2) :
  `gcc -O3 -march=native -fopenmp -o dctsolve tools/dct_solver.c -lm` ; modes `dict` (phrases → K2),
  `withk2` (K2 donnée → K1 par recuit), `solvepair`, `ctrlpair` (longueur `DCT_N`), note PMI avec `DCT_PMI=1`.
- `tools/build_qg.py` : modèle de quadrigrammes (`data/models/qg_en.bin`, 15 M lettres de 16 romans anglais du
  XIXᵉ siècle, Gutenberg ; *Frankenstein* réservé aux contrôles : `data/heldout/en_frankenstein.txt`).
