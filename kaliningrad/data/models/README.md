# Modèles de langue (quadgrammes joints) et textes réservés aux contrôles

- `qg_<langue>.bin` : 456 976 flottants (float32, petit-boutiste), QG[((a·26+b)·26+c)·26+d] = ln(compte/N),
  plancher ln(0,01/N) ; construits par `tools/build_qg_joint.c`.
- `qg_de.bin` est entraîné sur *Faust: Der Tragödie erster Teil*, *Effi Briest* et
  *Kritik der reinen Vernunft* (Project Gutenberg nos 2229, 5323 et 6343).
- `../heldout/<langue>.txt` : textes réservés (A-Z), jamais utilisés pour construire les modèles
  (`en` = *Alice* ; autres langues tronquées à 300 000 lettres).
- `heldout/de.txt` est extrait de *Die Verwandlung* (Project Gutenberg no 22367),
  séparément du corpus d'entraînement.
- Empreintes : `../SHA256SUMS_models.txt`.
