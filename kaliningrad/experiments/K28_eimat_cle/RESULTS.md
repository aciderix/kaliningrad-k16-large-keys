# K28 — « eimat » / « Heimat » comme clé, et autres pistes rapides (2026-10-03)

Statut : test direct, calibré par 300 mélanges des lettres de la bouteille. Outil : `tools/k28/eimat.py` (≈ 1 min) ;
sortie : `logs/eimat.out`.

## Question

Le mot isolé « eimat » qui suit le dernier bloc (puis une rangée de points) a été lu comme « Heimat ». Un mot écrit
à part à la fin d'un cryptogramme est souvent la **clé**. Les recherches exhaustives ou par recuit (K03, K06–K09,
K13–K15, K19) couvrent déjà ces cas, mais sans jamais poser la question explicitement ; on la pose ici.

## Procédés essayés

Clés `eimat`, `heimat` et leurs miroirs `tamie`, `tamieh` ; ordre de la clé à l'endroit et à l'envers :
colonnes à clé (déchiffrement et chiffrement), double transposition avec la même clé, les mêmes par bloc
(166, 169, 162, 169, 169, 144) ; Vigenère, Beaufort et Vigenère inverse ; zigzag à 5 et 6 rails (texte entier et par
bloc). Note : quadrigrammes allemands moyens (`qg_de.bin`, avec le plancher du modèle) ; un clair allemand donne
≈ −10, ≈ −11 avec 10 % de nuls ; la bouteille telle quelle −15,47.

## Résultat

Tous les résultats tombent **au niveau des lettres mélangées** (−15,1 à −15,8 contre −15,6 en moyenne pour les
mélanges ; −18 pour les chiffres polyalphabétiques, qui brouillent les lettres). Le meilleur rang (double
transposition par bloc avec `heimat`, −15,15) reste à 5 unités d'un texte allemand ; les quelques rangs ≈ 0,03 des
« chiffrements » reflètent le léger reste d'ordre local (K19, K23), pas un clair. Aucun début de résultat n'est lisible.

### Le seul écart : double transposition par bloc avec `heimat` (vérifié, non significatif)

Ce cas obtient −15,15 contre −15,63 ± 0,16 pour 3 000 mélanges (p = 0,001), et `heimat` se classe **4ᵉ sur les
720 clés possibles de largeur 6** pour ce procédé sur la bouteille (`logs/heimat_bloc_controle.out`). Mais :
- 40 combinaisons clé × procédé ont été essayées : avec cette correction, p ≈ 40 × 4/720 ≈ 0,2 ;
- sur des mélanges de la bouteille, la **meilleure** des 720 clés atteint en moyenne −15,17 : `heimat` ne fait que
  le niveau qu'une clé quelconque atteint sur des lettres au hasard ; sur la bouteille, toutes les clés sont un peu
  relevées par le reste d'ordre local (K19 : signal aux distances 1–40 ; ce procédé juxtapose des lettres distantes
  de 4, 14 ou 23 positions dans la bouteille) ;
- le résultat reste à 5 unités d'un texte allemand et n'a aucun passage lisible.
C'est une curiosité statistique, pas un indice de clé.

## Complément : lire la page manuscrite en colonnes (`tools/k28/pagecols.py`, `logs/pagecols.out`)

Les routes de K06 découpent le flux en largeurs fixes ; ici on prend les **lignes réelles** du manuscrit (35 à
46 lettres) comme rangées et on lit la k-ième lettre de chaque ligne, k = 1, 2, … (vers le bas ou vers le haut, en
alternance ou non ; position comptée en lettres ou en caractères, espaces compris, pour suivre l'alignement visuel ;
page 1, page 2, les deux). 24 lectures, chacune comparée à 300 jeux de lignes de mêmes longueurs remplies au hasard
avec les lettres de la bouteille : toutes au niveau des témoins (−15,0 à −16,1 ; rangs 0,02 à 0,99, comme attendu sur
24 essais), aucune suite lisible. Le texte n'a pas été écrit en colonnes sur la page.

## Complément : les signes de l'habillage marquent-ils des nuls ? (`tools/k28/marques.py`, `logs/marques.out`)

Si l'auteur avait glissé des lettres nulles dans un texte resté dans l'ordre en les signalant, les retirer rendrait
les liens entre voisines. Lettres retirées → information mutuelle entre voisines (z contre 400 mélanges) :
aucune (+0,01), les 117 lettres apostrophées (+0,89), les 41 n' seuls (+0,37), les 26 lettres accentuées (+0,09),
les 28 lettres des abréviations (0,00), apostrophées et accentuées (+0,53). **Aucun retrait ne fait apparaître de
liens** ; les notes de quadrigrammes restent au niveau des mélanges. Les marques ne désignent pas des nuls dans un
texte lu dans l'ordre.

## Outil : vérifier une proposition de solution (`tools/k28/verifier.py`)

Pour toute « solution » annoncée (clair allemand ou autre) : bilan des lettres (nuls nécessaires ; lettres du clair
absentes de la bouteille, qui excluent toute transposition), déplacement maximal D à admettre pour passer du clair
à la bouteille si les lettres n'ont bougé que localement (appariement dans l'ordre, glouton optimal), et la même
mesure sur 200 fenêtres d'allemand sans rapport de même longueur. Une proposition qui ne fait pas nettement mieux que
ces fenêtres n'est qu'un texte compatible parmi d'autres (K22). Exemple : un message inventé de 88 lettres
(« Wir sind hier in Pillau und denken an die Heimat… ») donne D = 190, exactement le niveau des fenêtres
quelconques (médiane 187).

## Conclusion

« eimat » / « Heimat » n'est la clé d'aucun de ces procédés. Le mot reste inexpliqué : signature, dernier mot laissé
en clair, ou élément de l'habillage. Les clés-mots en général (dictionnaires allemand et russe, doubles
transpositions comprises) sont traitées en K27.
