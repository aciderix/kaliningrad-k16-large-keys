# D01 — Étalonnage sur le défi de 2007 (résolu par G. Lasry en 2013) (2026-10-04)

But : vérifier que notre chaîne (IDP de Lasry, porté de CrypTool 2 en C) résout une vraie double transposition à
clés de 21 et 23, avant de s'en servir sur Reloaded.

## 1. Recuit aveugle sur K2 : échec
Solveur hérité de Kaliningrad K16 (`tools/dct_solver.c`), largeurs connues 21×23 :
- défi réel : −13,8 par quadrigramme (illisible), dans les deux ordres de largeurs ;
- 3 contrôles plantés (Frankenstein, 599 lettres, 21×23) : 0/3. La vraie K2 a une IDP de 0,38–0,41, mais le recuit
  s'arrête vers 0,135 : **c'est la recherche qui échoue, pas la note** (le paysage est presque plat loin de la clé).
  Le passage de la note au log-rapport des bigrammes (information mutuelle ponctuelle, `DCT_PMI=1`) ne change rien.

## 2. Attaque par dictionnaire de phrases (méthode de CrypTool 2) : succès
Le modèle CrypTool 2 « Dictionary attack on the Double Columnar Transposition » (`Templates/Cryptanalysis/Classic/
IDPAttack.cwm`, licence Apache 2.0) utilise exactement ce défi et une liste de 17 514 expressions anglaises
(`data/ct2_keyphrases.txt`, issues de COCA). Notre mode `dict` note chaque phrase comme K2 (rang alphabétique, ex aequo
de gauche à droite), pour chaque largeur w1 de 15 à 30 :

| Phrase | w1 | IDP |
|---|---:|---:|
| **preponderance of evidence** | **21** | **0,367** |
| la même, autres largeurs | 28–29 | 0,245–0,247 |
| meilleure autre phrase | 29 | 0,241 |

Puis K1 par recuit (quadrigrammes anglais, `withk2`, 8 × 50 000) : note −9,59 et clair lisible :

« THE GIRL HAD ARRIVED AT LUPTON HOUSE A HALF HOUR AHEAD OF MISS WESTMACOTT AND UPON HER ARRIVAL SHE HAD EXPRESSED
SURPRISE EITHER FEIGNED OR REAL AT FINDING RUTH STILL ABSENT … »

(personnages de *Mistress Wilding*, R. Sabatini, 1910 — le « roman peu connu du XIXᵉ siècle » de K. Schmeh est en
fait de 1910). K1 (21) n'est pas une phrase de la liste ; elle est retrouvée par recuit.

## 3. Conséquences pour Reloaded
- Le recuit aveugle ne suffit pas à 21×23 ; il suffira encore moins à 20–34. Lasry le dit aussi (commentaire de 2018).
- **L'IDP d'une K2 correcte se détache nettement** (0,37 contre 0,25 pour le meilleur concurrent parmi 560 000 essais) :
  une attaque par dictionnaire a toute la puissance voulue, *si la phrase est dans le dictionnaire*.
- La liste de CrypTool 2 appliquée à la partie 1 : maximum 0,19 (niveau du bruit), pas de clé (`logs/dict_ct2_part1.out`).
