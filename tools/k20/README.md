# Outils K20 (blocs et mots)

Bibliothèques : `tools/k18/` (common, dewin), `tools/k19/` (periodic). Corpus : `K18_CORPUS` (voir `tools/k18/fetch_corpus.sh`).
Lancer depuis un dossier de travail (les flux de contrôle `wc_*.txt`, `ps_*.txt` y sont écrits).

| Script | Section de `experiments/K20_blocs_et_mots/RESULTS.md` |
|---|---|
| `sections.py`, `underlined.py` | § 1 (frontières de sections, lettres soulignées) |
| `wordspot.py <k> <mélanges>` | § 2 (repérage de mots dans la bouteille) |
| `wc_gen.py`, `wordspot_file.py <k> <mélanges> <flux>` | § 2 (contrôles de puissance) |
| `wordlang.py` | § 2 (vocabulaires d'autres langues) |
| `twoaxes.py ['motif']`, `pseudo_gen.py` | § 3 (paires et mots ; pseudo-allemand de Markov) |
| `asym.py` | § 4 (sens de lecture) |
