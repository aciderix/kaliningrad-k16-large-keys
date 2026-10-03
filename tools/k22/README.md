# Outils K22 (reconstruction sans source)

`K18_CORPUS` doit pointer vers le dossier `corp/` (corpus K18) ; son dossier parent doit contenir `gut/` (livres
allemands de Gutenberg, voir `tools/k21/`). Lancer depuis un dossier de travail.

| Script | Rôle |
|---|---|
| `buildlm.py` | modèle de mots (unigrammes, paires) sur 420 livres, Kafka exclu → `lm.pkl` |
| `wdecode.py` | décodeur mot à mot sous contrainte de déplacement (faisceau) |
| `ctrl22.py s L faisceau` | contrôle : L lettres de Kafka déplacées d'au plus s positions, décodage, comparaison |
| `cribcheck.py` | mots devinés : fréquence de « logement » dans la bouteille contre des mélanges |
| `unicity.py` | information portée par la composition de tranches de n lettres |
