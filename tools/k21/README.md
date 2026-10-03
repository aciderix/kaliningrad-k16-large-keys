# Outils K21 (échelle du brassage, nuls, texte source)

Bibliothèques : `tools/k18/`, `tools/k19/`. Corpus : `K18_CORPUS` ; corpus élargis :
- Gutenberg allemand : `gutenberg_de_ids.txt` (catalogue 2026), téléchargement `dl_gutenberg.sh <id>` ;
- chants : `dl_volkslieder_api.sh <page>` (API WordPress de volksliederarchiv.de, pages 1–113), puis `songs_extract.py` ;
- Bible de Luther 1912 : https://ebible.org/Scriptures/deu1912_readaloud.zip.

| Script | Section de `experiments/K21_source_et_echelle/RESULTS.md` |
|---|---|
| `abc.py`, `abc2.py`, `abc3.py` | § 1 (échelle du brassage, simulation ABC) |
| `skipgram.py` | § 2 |
| `nullid.py` | § 3 |
| `srcalign.py`, `srcscan.py <fichiers>`, `shortalign.py ctrl|scan <fichiers>`, `shortcal.py` | § 4, 4 bis (recherche du texte source) |
| `grille_sa.c` (`gcc -O3 -fopenmp -o grille_sa tools/k21/grille_sa.c -lm` ; `grille_sa n P.txt flux.txt 4 150000 1`) | § 5 |
| `fragments.py` | § 6 |
