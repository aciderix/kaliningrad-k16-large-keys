# Modèles de langue (quadgrammes joints) et textes réservés aux contrôles

- `qg_<langue>.bin` : 456 976 flottants (float32, petit-boutiste), QG[((a·26+b)·26+c)·26+d] = ln(compte/N),
  plancher ln(0,01/N) ; construits par `tools/build_qg_joint.c`.
  - `en` : corpus Gutenberg anglais de 13,6 M lettres (hérité de `kryptos/`), *Alice* (Gutenberg n° 11) exclue.
  - `fr de it es la nl eo` : livres Gutenberg (liste : `experiments/E05_languages/logs/corpus.txt`), en-têtes
    retirés, accents supprimés, A-Z ; un livre par langue réservé aux contrôles.
- `../heldout/<langue>.txt` : textes réservés (A-Z), jamais utilisés pour construire les modèles
  (`en` = *Alice* ; autres langues tronquées à 300 000 lettres).
- Empreintes : `../SHA256SUMS_models.txt`.
