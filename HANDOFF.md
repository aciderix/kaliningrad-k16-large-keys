# Passage de relais (2026-10-04) — à lire en premier

## Directives de l'utilisateur
1. **Lire l'existant avant de chercher** : dépôt de D. Bourdeau https://github.com/dbourdeau/cyphersolver (en particulier
   `targets/blume/NOTES.md`, et les autres cibles), travaux de G. Lasry, CrypTool 2 (code IDP, modèles, listes de
   phrases), blog Cipherbrain de K. Schmeh et ses commentaires. Noter dans le README de la cible ce qui est déjà exclu
   par d'autres, pour ne jamais le recalculer.
2. **Être intelligent, pas brutal** : chercher les schémas et la structure du problème (deux messages sous la même
   clé, mots probables, géométries de rectangle complet, régularités de dérivation des clés) avant tout calcul long.
   Éviter les approches qui coûtent des heures.
3. **C et outils ultra performants dédiés** ; partir de ce que la communauté a déjà (CrypTool 2, solveurs de Lasry,
   AZdecrypt, KenLM…) plutôt que réinventer la roue.
4. **Approches peu traditionnelles bienvenues** si on estime qu'elles peuvent aider, à condition de les tester vite sur
   un contrôle planté.
5. Garder la rigueur : pré-inscription commitée avant le résultat, contrôles plantés, seuil de décision fixé à l'avance.
   Un calcul long seulement s'il est justifié (contrôle + estimation de durée) ; au-delà de ~30 min, GitHub Actions.

## État
| Dossier | Statut |
|---|---|
| `kaliningrad/` | close (K01–K30 ; pseudo-texte le plus probable ; `kaliningrad/docs/03_bilan.md`) |
| `richelieu_decode/` | abandonnée : déjà déchiffrée (Avenel 1858, vérifié par Bourdeau) |
| `dct_reloaded/` | D01 : défi Schmeh 2007 cassé par dictionnaire de phrases (K2 = « preponderance of evidence », w1 = 21) ; recuit aveugle sur K2 : échec (vraie IDP 0,41, recherche bloquée à 0,135). D02 : partie 1, K2 n'est aucune suite de mots de Wikiquote anglais (121 M clés, IDP max 0,209 contre 0,40–0,45 pour une vraie clé). Lasry avait exclu Wikipédia + Gutenberg (2018). |
| `blume_salamanca/` | B01 : K2 n'est aucun début de phrase de Wikiquote es/de (5,4 M clés, max 0,185 contre 0,35–0,36). Ouvert selon Bourdeau : double transposition directe, deux clés ≥ 11 (w2 ≤ 10, w1 ≤ 41 exclus par lui). Piste la plus prometteuse : **attaque conjointe des deux télégrammes** (615 + 160 lettres, mêmes clés probables), cribs commerciaux. |

## Outils
- `dct_reloaded/tools/dct_solver.c` : modes `dict`, `stream` (dictionnaire en flux ; `DCT_W1`, `DCT_ANYW`,
  `DCT_OFFMAX`), `withk2` (K2 donnée → K1 par recuit), `solvepair`, `ctrlpair` ; `DCT_PMI=1` pour la note PMI.
  `tools/plant.py` : contrôles plantés.
- Modèles : `dct_reloaded/data/models/qg_en.bin`, `blume_salamanca/data/models/qg_es.bin` ; textes réservés dans
  `data/heldout/`.
- `.github/workflows/phrase-scan.yml` + `.github/scan/job.env` : modifier `job.env` et pousser lance 20 machines
  (clés générées par `common/phrasekeys.py` depuis un dump Wikiquote, réparties par crc32).

## Pièges rencontrés
- Le conteneur peut redémarrer et tuer les processus : processus détachés (`setsid nohup`) et tranches reprenables.
- Les commandes d'arrière-plan de l'outil sont coupées après 2 h.
- `pkill -f` avec un motif présent dans sa propre ligne de commande tue le shell appelant.
