# K07 — Recherche de la transposition avec un score **insensible à la substitution** (information mutuelle) — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul (2026-09-29).

## Pourquoi
K03, K05, K06 notent les candidats en quadrigrammes allemands : ils supposent les lettres intactes. Or K02 laisse ouverte
l'hypothèse C (transposition **et** substitution), que l'excès de f/w rend plausible. L'information mutuelle entre lettres
voisines MI(1) (K02) est **invariante par toute substitution simple** et quelle que soit la langue : la bonne remise en ordre doit
la faire remonter au niveau d'une langue (contrôles K02 : z ≈ 37-40 sur 984 lettres).

## Familles testées
1. **Routes** : catalogue exhaustif de K06 (28 routes × lecture/inverse × largeurs 2..n/2), sur chaque bloc S1..S6 et sur le texte
   entier (979 lettres).
2. **Grille carrée à clé** (V1/V2 de K03) sur S2, S4, S5, S6 : montée avec redémarrages maximisant MI(1).
3. **Transposition en colonnes à clé sur le texte entier** (écriture en lignes de w lettres, dernière ligne incomplète, colonnes
   lues dans l'ordre de la clé), w = 5..20 : montée avec redémarrages maximisant MI(1), dans les deux sens (V1 et inverse).
Score : MI(1) (bits, estimateur direct) du texte candidat, variante A.

## Contrôles (avant le texte)
Texte allemand réservé, **substitution simple aléatoire**, puis transposition tirée dans la famille (10 essais par famille et
taille) ; succès = ≥ 90 % des lettres voisines recollées ; exigé ≥ 8/10, sinon la famille est déclarée sans puissance (rapporté).
Nuls : permutations aléatoires des lettres de la suite réelle, même recherche (100 pour les routes, 50 pour les familles 2-3).

## Décision
Une suite répond si son MI maximal dépasse tous ses nuls ; la remise en ordre trouvée est alors examinée : ses contacts doivent
atteindre le niveau d'une langue (z ≥ 10 contre des mélanges), et le texte doit ensuite être attaqué comme une substitution simple
(cellule suivante). Aucune revendication sans texte lisible.

## Amendement 1 (avant tout calcul sur le texte réel des familles 2-3)
- MI(1) est identique pour un texte et son inverse : le critère de succès des contrôles accepte le clair retrouvé à l'envers
  (lettres voisines recollées dans un sens ou dans l'autre), comme en K05.
- La montée simple échoue sur la famille 3 en sens V1 (colonnes de longueurs inégales) : recherche remplacée par un **recuit
  simulé** (T de 0,02 à 0,0005 bit), effort fixé sur les contrôles puis gelé.
- Famille 1 (routes) : contrôles des blocs 4/10 (169) et 4/10 (144) ⇒ **sans puissance sur les blocs** ; texte entier 8/10.

## Amendement 2 — extension aux clés longues (2026-09-29, avant calcul sur le texte réel)
Famille 3 étendue à w = 21..40 (texte entier), recuit 5 × 20 000. Essai de puissance (3 textes allemands substitués) : 2/3
retrouvés en entier, le 3e (sens V1) recolle 67 % des contacts avec MI = 0,69, très au-dessus du niveau des mélanges (≈ 0,44) ⇒
**décision fondée sur la détection** : le texte répond si son MI dépasse ses nuls (30) et atteint ≥ 0,6.
