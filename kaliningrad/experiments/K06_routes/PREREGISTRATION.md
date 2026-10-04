# K06 — Transpositions par routes classiques, recherche exhaustive (sections et texte entier) — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul (2026-09-29).

## Pourquoi
Les routes sans clé (spirales, diagonales, zigzags, colonnes) ne créent pas de contact à distance fixe : K02 ne les exclut pas,
K03/K05 non plus. Elles sont en nombre fini : on peut toutes les essayer.

## Modèle
Suite chiffrée de n lettres (variante A de v1) : chacune des 6 sections, et le texte entier (984 lettres, sections à la suite).
Pour chaque largeur w = 2..⌊n/2⌋ : le chiffré est écrit en lignes de w (dernière ligne incomplète), puis lu selon une route ;
et l'opération inverse (clair écrit selon la route, chiffré lu en lignes). Routes : colonnes (gauche→droite, droite→gauche,
vers le bas ou le haut), colonnes en zigzag (4), lignes en zigzag (2), diagonales (4 coins × 2 sens), spirales (4 coins × 2 sens,
vers l'intérieur ; vers l'extérieur = clair à l'envers). Chaque résultat est aussi lu à l'envers.
Score = moyenne des quadrigrammes allemands (`qg_de.bin`), outil `tools/k06_routes.py`.

## Contrôles
(a) Pour chaque taille (169, 144, 984) : 10 textes allemands réservés chiffrés par une route et une largeur tirées au hasard dans
le catalogue ; la recherche doit retrouver la bonne (score maximal) dans ≥ 9 cas sur 10.
(c) Nuls : 100 permutations aléatoires de chaque suite réelle ; même recherche ; maximum du catalogue.

## Décision
Une suite répond si son meilleur score dépasse ses 100 nuls (p < 0,01 ; 7 suites testées ⇒ p global < 0,07, noté) ; tout
résultat imprimé ; revendication seulement sur texte lisible.
