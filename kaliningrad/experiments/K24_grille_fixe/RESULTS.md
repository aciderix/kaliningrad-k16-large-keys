# K24 — Grille à trous fixe (Cardan non tournante) (2026-10-03)

Statut : exploration calibrée. Outil : `tools/k24/cardan.py` ; sorties : `logs/`.

## Hypothèse
Une grille percée de trous est posée sur chaque bloc de p cases ; le message est écrit dans les trous, dans l'ordre
de lecture, et les autres cases sont remplies de lettres quelconques. Avec la même grille pour tous les blocs, les
lettres du message occupent les mêmes positions dans chaque bloc. Cette famille n'avait jamais été testée (K05, K19,
K21 ne portaient que sur les grilles **tournantes**, qui ne laissent aucune case de remplissage).

## Méthode
Pour chaque taille de bloc p (25 à 169) et chaque proportion de trous (25 %, 40 %, 60 %), recherche **exacte** (programmation
dynamique) du chemin croissant de m positions qui maximise le score de bigrammes allemands entre trous consécutifs,
moyenné sur tous les blocs ; 8 décalages de départ ; témoins : lettres de la bouteille mélangées.

## Résultats
Contrôles (message allemand dans des trous plantés, remplissage = lettres de la bouteille) : +0,51 à +0,61, contre
au plus −0,20 à +0,39 pour les lettres mélangées. Bouteille (`logs/cardan_real.out`) : toujours dans la zone des
mélanges ou juste au-dessus (le cas le plus proche, p = 169 et 25 % de trous : +0,47 contre +0,46 au mieux pour les
mélanges et +0,61 pour une grille plantée), léger excédent attendu de l'arrangement des lettres dans les mots (K23).

## Conclusion
Aucune grille à trous fixe commune aux blocs (blocs de 25 à 169 cases, 25 à 60 % de trous) ne cache un message
allemand. Restent non couvertes : des grilles différentes pour chaque bloc et des grilles posées sur la page entière
avec un ordre de lecture autre que ligne par ligne.
