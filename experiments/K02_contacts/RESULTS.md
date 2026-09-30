# K02 — RÉSULTATS (2026-09-28) : **aucun contact entre lettres voisines** — le texte n'est pas une langue naturelle lue dans l'ordre sous une substitution lettre à lettre

Pré-inscription : `PREREGISTRATION.md` (commit 0a39ef5). Outil : `tools/k02_contacts.py` ; sorties : `logs/controles.out`,
`logs/reel.out`. Texte de contrôle : `data/controle_de_kant_6343.txt`.

## 1. Contrôles (allemand réservé, 984 lettres, mêmes sections)
| Contrôle | T5 p(1) (z) | pic | T6 p |
|---|---|---|---|
| (a) clair | 0,0005 (**z = 37**) | d = 1, 2, 3 | |
| (b) substitution simple | 0,0005 (**z = 40**) | d = 1, 2, 3 | |
| (c) carrés 13×13 / 12×12, colonnes à clé | 0,37 (z = 0,3) | aucun | |
| (d) carrés, colonnes dans l'ordre | 0,43 (z = 0,2) | **d = 13 (z = 18)**, 26, 39 | |
| (e) vrais mots allemands sous substitution | | | **0,008** |
| (f) texte (c) recoupé en faux mots | | | 0,89 |
Tous conformes ⇒ T5 et T6 ont la puissance voulue (T6 de justesse).

## 2. Texte réel (v1)
| Données | T5 p(1) (z) | p(12) | p(13) | plus fort z (40 distances) |
|---|---|---|---|---|
| S1-S6 | **0,32 (z = 0,5)** | 0,49 | 0,49 | d = 15 : z = 2,0, p = 0,03 (non significatif après correction ×40) |
| S1-S5 | 0,16 (z = 1,0) | 0,50 | 0,49 | d = 18 : z = 2,3 (idem) |
| S6 seule (carré 12 ?) | 0,038 (z = 1,8) | 0,60 | — | — |
T6 (194 mots) : χ² = 126,5, **p = 0,002**.

## 3. Conclusions (RÉSULTAT)
1. **Les lettres voisines du chiffré ne sont pas liées entre elles** (z = 0,5 contre 37 à 40 pour de l'allemand clair ou chiffré par
   substitution). Ce test ne suppose aucune langue : **une langue naturelle écrite dans l'ordre, même sous une substitution simple
   (quelle que soit la langue : russe translittéré, ukrainien, finnois, allemand…), est exclue.** Ceci élimine d'un coup la
   famille d'hypothèses la plus débattue (Cipherbrain 2016-2017, commentaires russes 2015). Pas trouvé dans les sources lues.
2. **Pas de grille carrée lue colonne par colonne dans l'ordre** (aucun pic à 13 ni à 12). Une grille **à clé** reste possible :
   ce test ne la voit pas (contrôle c).
3. **Les espaces ne sont pas des coupures au hasard** (p = 0,002). Cela tient surtout à trois choses : le mot d'une lettre « i »
   (7 fois, alors que e, deux fois plus fréquent, est seul 3 fois), et n et t plus souvent en fin de mot.

## 4. Explorations après coup (déclarées comme telles, sans valeur de preuve)
- Robustesse : même absence de contacts avec l'apostrophe comptée comme signe distinct (35 signes : z = −0,4) et **à l'intérieur
  des mots** (z = 1,6, p = 0,05) — moins encore que de l'allemand dont on a anagrammé chaque mot (z = 4,0).
- Fréquences (seule chose qu'une transposition conserve) comparées à 7 langues (blocs de 984 lettres des corpus d'entraînement) :
  | Langue | χ² fréquences brutes (seuil 99 %) | profil trié : p |
  |---|---|---|
  | allemand | **147** (114) | **0,13** |
  | néerlandais | 471 (127) | 0,002 |
  | français, italien, espagnol, latin, espéranto | ≥ 4 655 | ≤ 0,003 |
  Seul l'allemand a un profil trié compatible ; mais ses fréquences brutes ne collent pas : excès de **f** (46 contre 15 attendus)
  et **w** (36 contre 17), déficit de b, g, c, a. Le russe translittéré est exclu en transposition simple (o ≈ 11 % attendu, 0,9 %
  observé).

## 5. Ce qui reste (HYPOTHÈSES)
- **A** : un texte allemand (ou proche) dont les lettres ont été **permutées** sur de grands blocs (grille à clé, route…),
  avec peut-être quelques changements de lettres ; espaces et apostrophes ajoutés ensuite pour faire « langue ».
- **B** : un **pseudo-texte** (pas de message) : lettres choisies avec des fréquences imitant l'allemand, sans enchaînement, avec
  des « mots » et des apostrophes d'aspect étranger.
Test suivant proposé (K03) : recherche de clés de colonnes par section (13 ou 12 colonnes) notée par quadrigrammes allemands, en
C, **calibrée d'abord** (retrouve-t-elle une clé sur 169 lettres ? que trouve-t-elle sur un texte mélangé au hasard ?).
