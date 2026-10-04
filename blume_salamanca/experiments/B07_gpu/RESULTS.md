# B07 — Dictionnaires sur GPU (Kaggle, 2 × T4)

**Outil.** `tools/bdt_gpu.cu` : port CUDA du mode `dict` de `bdt.c` (IDP de T1 pour chaque w1 = 11–30, clé unique
aux quadrigrammes T1 + T2), les **deux numérotations** (ex aequo de gauche à droite, variante 0 ; de droite à gauche,
variante 1). Notebooks : `kaggle/run_controls.py`, `kaggle/run_dict.py`.

**Contrôles plantés (GPU, 20 000 clés, 4 oct. 2026, version 2 du notebook de contrôle).**

| contrôle | clé plantée | GPU | CPU (bdt.c) |
|---|---|---|---|
| deux clés (`pc`) | « dennmeinvol », w1 = 16, w2 = 11 | z = 24,1 | 21,3 |
| ex aequo de droite à gauche (`pt`) | « dariefderkonigisraelsa », w1 = 11, w2 = 22, variante 1 | z = 21,4 | 22,4 |
| clé unique (`ps`) | « dennmeinvol » | z = 25,9 | 25,1 |

Meilleure fausse clé ≈ 5 dans les trois cas (écarts GPU/CPU : échantillon des clés aléatoires de référence).
Débit : ≈ 9 000 clés/s par T4 avec les deux variantes (≈ 18 000 essais clé × variante / s). Bogue corrigé avant
validation : boucle infinie au dernier tour de la chaîne gloutonne (cycle refermé).

**Production (`run_dict.py`, seuil pré-inscrit z ≥ 9)** : (1) Bibles de/es + 33 œuvres (comme B02, ≈ 10,4 M clés) ;
(2) Wikiquote de/es (débuts, troncatures, fenêtres) ; (3) les 3 290 livres Gutenberg allemands et espagnols (mots
entiers). Résultats : à compléter.
