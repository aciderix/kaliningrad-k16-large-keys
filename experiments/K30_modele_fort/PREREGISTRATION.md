# K30 — Grille tournante indépendante par bloc, avec nuls, notée par un modèle 6-grammes : pré-inscription
(2026-10-04, commitée après les contrôles et avant tout calcul sur la bouteille)

## Hypothèse
Chaque bloc carré de la bouteille — S2, S4, S5 (169 = 13×13) et S6 (144 = 12×12) — est un clair de type allemand
contenant ≈ 10 % de nuls, chiffré par une grille tournante (Fleissner) **avec une clé propre au bloc**. C'est la seule
famille que K05 et K29 déclaraient non testable (quadrigrammes : clé retrouvée 2/12 et 4/12 avec 10 % de bruit).

## Outil
- Modèle : 6-grammes de lettres (contexte de 5), Witten-Bell jusqu'à l'unigramme, mélange tolérant aux nuls
  P' = 0,9·P + 0,1/26 (`tools/k30/build_lm6.c`), appris sur 8,9 millions de lettres de 20 livres allemands de
  Gutenberg (corpus K18), **Kafka (*Die Verwandlung*, texte des contrôles) exclu**. Allemand réservé : −1,51 nat par
  lettre ; avec 10 % de nuls −2,26 ; lettres mélangées −4,10.
- Recherche : `tools/k30/fleiss_lm.c` (dérivé de K05 : 8 variantes, recuit, R = 6 redémarrages × I = 100 000).

## Contrôles (faits avant la bouteille ; `logs/ctrl_*.out`)
Kafka + 10 % de nuls f/w/n **insérés**, une grille et une variante tirées au hasard par bloc ; succès = ≥ 90 % des
voisinages retrouvés.

| | 13×13 | 12×12 |
|---|---:|---:|
| quadrigrammes (K05) | 1/12 | 3/12 |
| **6-grammes tolérant aux nuls** | **10/12** | **9/12** |

Notes trouvées sur les contrôles : −2,05 à −2,80 par lettre (22/24 au-dessus de −2,6).

## Protocole sur la bouteille (fixé maintenant)
Pour chacun des 4 blocs carrés : même recherche sur le bloc réel et sur **20 mélanges** de ses lettres.
- Un bloc est déclaré **chiffré par grille tournante** si sa note dépasse les 20 mélanges **et** atteint −2,6, avec un
  texte lisible.
- Si aucun des 4 blocs ne remplit ces conditions, l'hypothèse « grille tournante indépendante par bloc, avec ≈ 10 % de
  nuls » est **exclue** pour les blocs carrés (puissance par bloc ≈ 0,8, et 22/24 contrôles au niveau −2,6).
- S1 (166) et S3 (162) ne sont pas des carrés pleins : hors du test.
