# K11 — Identification de la règle de placement des espaces — PRÉ-INSCRIPTION

Rédigée et commitée avant tout ajustement de modèle (2026-09-29). Déjà connu (K10, exploration) : les frontières évitent la paire
consonne|voyelle (z = −6 contre l'ordre des mots mélangé), excès de V|V, C|C et lettres identiques ; tableau des taux par
catégorie de paire.

## Question
Existe-t-il une règle **locale** simple qui décide où l'auteur coupe, et laquelle ? En particulier : la décision dépend-elle
seulement des deux lettres voisines (interaction lettre d'avant × lettre d'après), ou d'une fenêtre plus large (±2), ou de
l'identité des lettres, de la position dans la ligne ?

## Données
Flux de lettres de `data/transcription_v1.txt` (variante A : a-z, accents fusionnés ; lignes L01-L25, « eimat » exclu).
Unité = jonction entre deux lettres consécutives d'une même ligne ; étiquette = espace ou non. Exclues : jonctions internes aux
abréviations (points) et fins de ligne (contrainte de mise en page ; analyse de sensibilité en les incluant comme coupures).

## Modèles (régression logistique, ridge λ = 1, tous avec la longueur écoulée depuis la dernière coupure, classes 1..7, 8+)
- M0 : longueur seule.
- M1 : M0 + classe (voyelle/consonne) de la lettre d'avant + classe de la lettre d'après (effets **séparés**).
- M2 : M1 + **interaction** (V|V, C|C) + lettre identique. ← règle d'habillage suggérée par K10.
- M3 : M0 + **identité** de la lettre d'avant + identité de la lettre d'après (effets séparés ; ce qu'a une vraie langue).
- M4 : M3 + interaction + lettre identique.
- M5 : M2 + classes des lettres à ±2 et leurs interactions avec les voisines (grappes CCC, VVV).
- M6 : M2 + position dans la ligne (tiers).

## Évaluation (validation sur des frontières jamais utilisées pour l'ajustement)
Validation croisée 2 plis : ajustement sur les lignes impaires, évaluation sur les paires, et l'inverse ; score = log-vraisemblance
totale hors échantillon. Gains d'intérêt : **G_int = LL(M2) − LL(M1)** et **G'_int = LL(M4) − LL(M3)** (interaction), **G_fen =
LL(M5) − LL(M2)** (fenêtre large), **G_pos = LL(M6) − LL(M2)**.
Nul : les mêmes gains calculés sur 1 000 versions du texte où **l'ordre des mots est mélangé** (conserve fins et débuts de mots et
longueurs, casse l'interaction à la frontière). p = part des nuls ≥ observé.

## Contrôles (avant le texte réel)
(a) **Plantés** : flux de lettres de la bouteille mélangé, espaces posés par une règle connue de type M2 (paramètres voisins de ceux
de K10) et par une règle sans interaction (type M1) ; la procédure doit trouver G_int significatif (p < 0,01) dans le premier cas,
non dans le second (≥ 8/10 chacun).
(b) **Textes réels** (allemand, russe, polonais, néerlandais ; 10 fenêtres de ~980 lettres chacun, espaces réels) : G_int doit y être
au niveau de son nul (p > 0,01 dans ≥ 80 % des fenêtres).

## Décision
- « Règle d'interaction à deux lettres » confirmée si G_int et G'_int ont p < 0,01 sur la bouteille (v1) **et** se retrouvent sur la
  transcription de Corsair_nv (p < 0,05).
- « Fenêtre plus large » retenue seulement si G_fen p < 0,01 ; sinon la règle est dite locale à deux lettres.
- Les paramètres ajustés de la meilleure règle sont rapportés (taux de coupure par catégorie).
Portée : identifie le procédé d'habillage, pas le chiffrement ; ne départage pas « chiffré maquillé » et « texte artificiel découpé ».
