# Third-party data and method notices

- `tools/k16_double_ct2.c` reimplements the IDP analysis and movement approach
  documented by CrypTool 2's `CrypPlugins/IDPAttack/IDPAnalyser.cs`, associated with
  Lasry, Kopal & Wacker, *Cryptologia* 38(3), 2014. The upstream CrypTool 2 project
  is distributed under Apache License 2.0: <https://github.com/CrypToolProject/CrypTool-2>.
- `data/models/qg_de.bin` and `data/heldout/de.txt` are copied from the local
  `dagapeyeff` research data bundle. The bundle's model documentation identifies
  German Gutenberg books as the training corpus and a separate held-out book for
  controls. See `data/models/README.md` and upstream provenance documentation before
  redistributing or reusing the corpora beyond this experiment.
- `data/transcription_v1.txt` is the project's transcription of the Kaliningrad
  bottle, with its sources and uncertainty documented in the file header and in
  the project research notes.
