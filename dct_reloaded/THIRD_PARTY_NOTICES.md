# Données et méthodes tierces

- `tools/dct_solver.c` dérive de `kaliningrad/tools/k16_double_ct2.c`, qui réimplémente l'évaluation IDP et les
  mouvements de `CrypPlugins/IDPAttack/IDPAnalyser.cs` (CrypTool 2, https://github.com/CrypToolProject/CrypTool-2,
  licence Apache 2.0) ; méthode : G. Lasry, N. Kopal, A. Wacker, *Cryptologia* 38(3), 2014.
- `data/ct2_keyphrases.txt` : copie de `Templates/Cryptanalysis/Classic/keyphrases.txt` de CrypTool 2 (Apache 2.0).
- `data/reloaded_part{1,2,3}.txt` : chiffrés des défis MysteryTwister « Double Column Transposition Reloaded » 1–3
  (A. Wacker, B. Esslinger, K. Schmeh, 2013), https://mysterytwister.org ; `data/calibration/` : chiffrés publiés par
  K. Schmeh sur Cipherbrain (2013, 2020).
- `data/models/qg_en.bin`, `data/heldout/en_frankenstein.txt` : construits à partir de textes du Project Gutenberg
  (domaine public aux États-Unis).
- Wikiquote (CC BY-SA 4.0) : seul l'outil d'extraction est versé ; les bases de clés se régénèrent depuis le dump.
