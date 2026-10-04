# Outils K19 (mélange local)

Bibliothèque commune : `tools/k18/common.py`, `tools/k18/dewin.py`. Corpus : `sh tools/k18/fetch_corpus.sh <dossier>`,
puis `export K18_CORPUS=<dossier>`.

```sh
gcc -O3 -march=native -o anagram  tools/k19/anagram.c  -lm   # anagramme d'une ligne (option D : déplacement maximal)
gcc -O3 -march=native -o chunkana tools/k19/chunkana.c -lm   # anagramme par tranches avec raccords
export K19_ANAGRAM=$PWD/anagram K19_CHUNKANA=$PWD/chunkana
python3 tools/k19/bandrep.py      # signal à courte distance, réplications et contrôles
python3 tools/k19/grille_real.py  # grilles tournantes 4×4–6×6, recherche exhaustive
```

| Script | Section de `experiments/K19_melange_local/RESULTS.md` |
|---|---|
| `periodic*.py` | § 2, permutation périodique (bigrammes ; MI) |
| `grille*.py`, `grille7.c` | § 2, grilles de Verne (7×7 en C : `gcc -O3 -fopenmp -o grille7 tools/k19/grille7.c` ; `grille7 7 P.txt flux.txt`, P = matrice 26×26 des log-rapports de bigrammes) |
| `perline.py`, `perline2.py` | § 2 et § 3.6, transpositions par ligne |
| `bigscore.py`, `bandrep.py`, `localnull.py` | § 3.1 |
| `scale.py` | § 3.2 |
| `cooc.py`, `ctest.py`, `cdist.py`, `bigdrivers.py` | § 3.3 |
| `vowelreg.py` | § 3.4 (prédiction fixée avant calcul) |
| `crossline.py`, `segheter.py`, `linechunk.py`, `chunkscan.py` | § 3.5 et § 3.9 |
| `anagram.c`, `dshape.py` | § 3.6–3.7 |
| `langband.py` | § 3.8 |
| `chunkana.c` | § 3.9 |
| `genre.py` | § 4 |
