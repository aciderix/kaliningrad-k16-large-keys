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
entiers). Résultats ci-dessous.

## Production : rien (4 octobre 2026, ≈ 4 h de notebook)
Contrôle planté au début du notebook : « dennmeinvol » retrouvé à z = 24,1 (meilleure fausse clé 5,1).

| source | clés | essais (w1 × variante + clé unique) | histogramme z > 4 | meilleur z |
|---|---:|---:|---|---:|
| Bibles de/es + 33 œuvres | 10,39 M | 436 M | [4,5) : 25 084 ; [5,6) : 481 ; [6,7) : 5 | 6,35 |
| Wikiquote de/es | 15,32 M | 643 M | [4,5) : 37 127 ; [5,6) : 663 ; [6,7) : 7 | 6,71 |
| Gutenberg de/es complet (3 290 livres) | 93,45 M | 3 925 M | [4,5) : 225 857 ; [5,6) : 4 362 ; [6,7) : 48 | 6,93 |

Rien au-delà de 7 sur ≈ 5 milliards d'essais : c'est la queue attendue du bruit (le maximum de N essais gaussiens
est ≈ √(2 ln N) ≈ 6,7). Meilleures clés : « alasaladelecturasalioalpatio » (w1 = 13, w2 = 28, variante 1),
« krankheittuberkulose », « forexamplecodehttpswwwwikidata » : du bruit. Gutenberg : 93,4 M de clés à ≈ 28 000 clés
par livre (mesuré sur 100 livres) ≈ 3 300 livres, donc la liste entière a bien été lue.

**Conclusion (seuil z ≥ 9).** Aucune phrase-clé (mots entiers, 11–30 lettres) des Bibles, des 33 œuvres, de Wikiquote
de/es ni des livres Gutenberg allemands et espagnols n'est K2 (w1 = 11–30) ou clé unique, dans aucune des deux
numérotations. Sorties : `logs/`.
