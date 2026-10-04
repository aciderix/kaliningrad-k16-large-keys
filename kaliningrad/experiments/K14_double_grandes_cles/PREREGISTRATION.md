# K14 — Double transposition à grandes clés (10-20 colonnes), attaque « diviser pour régner » — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul sur la bouteille (2026-09-29). Suite de K08 (clés 3-9 exclues ; recherche conjointe sans
puissance au-delà de 9 colonnes).

## Méthode (d'après Lasry, Kopal & Wacker 2014, « Solving the Double Transposition Challenge with a Divide-and-Conquer Approach »,
adaptée)
Clair P (979 lettres) → colonnes à clé K1 (w1) → T → colonnes à clé K2 (w2) → chiffré C.
1. **Étape K2** : pour une clé K2 candidate, on défait la seconde transposition (T' = inverse de K2 appliqué à C) ; si K2 est
   juste, T' est une simple transposition en colonnes du clair. On découpe T' en w1 colonnes (positions de départ estimées, décalages
   ±2 tolérés pour les colonnes longues/courtes) et on calcule un **potentiel de juxtaposition** : pour chaque colonne, le meilleur
   score de bigrammes allemands obtenu en la plaçant à gauche d'une autre colonne, ligne à ligne ; score(K2) = somme sur les colonnes.
   Ce score ne dépend pas de K1. Recuit simulé sur K2.
2. **Étape K1** : T' fixé, recherche de K1 par recuit (quadrigrammes allemands), comme une simple transposition.
Largeurs w1, w2 ∈ 10..20, inconnues (toutes les paires essayées). Outil : `tools/k14_double_idp.c`.
**Limite annoncée** : score fondé sur les bigrammes allemands, donc lettres supposées intactes (une substitution en plus n'est pas
couverte ; K08 la couvrait pour les clés courtes).

## Contrôles (avant la bouteille)
(a) Puissance à largeurs connues : 10 textes allemands réservés de 979 lettres, w1, w2 tirés dans 10..20 ; succès = ≥ 90 % des lettres
voisines recollées. (b) Même chose à largeurs inconnues. Exigé : ≥ 7/10 en (b), sinon le test est déclaré **sans puissance** et la
bouteille n'est pas interprétée (le résultat négatif ne vaudrait rien).
Nuls : 20 permutations aléatoires du flux réel, même recherche complète.

## Décision
La bouteille répond si le meilleur score final (quadrigrammes du clair candidat) dépasse ses nuls et atteint ≥ −10,5, avec un texte
lisible. Sinon : double transposition à clés de 10 à 20 colonnes (lettres intactes, allemand) exclue dans la mesure de la puissance
mesurée.

## Amendement 1 (avant tout calcul sur la bouteille)
- Attaque « diviser pour régner » (clés différentes, 10-20) : le score de juxtaposition reconnaît bien la vraie clé K2 (vraie −5,16 à
  −5,33 ; trouvée −5,5 à −5,8 ; aléatoire −5,8 à −6,1), mais la recherche ne la trouve que pour les petites largeurs (1/4 à largeurs
  connues, même avec 80 000 itérations et température réglée). ⇒ **déclarée sans puissance**, non appliquée à la bouteille.
- Ajout du cas historique **« même clé deux fois »** (Übchi, armée allemande 1914) : recherche conjointe sur une seule clé (outil K08,
  option `K08_SAME`), deux scores (quadrigrammes, lettres intactes ; MI, substitution admise). Essais à largeurs connues :
  quadrigrammes 3/3 pour 11-14 colonnes, 0/5 pour 16-19. **Portée fixée : 10-15 colonnes, largeur inconnue.** Contrôles : 10 textes par
  score, exigé ≥ 7/10 ; nuls : 20 ; décision : dépasser les nuls et atteindre le niveau de langue (−10,5 ; MI 0,7).
- Correction de l'outil K08 (initialisation du meilleur score à −1, inadaptée aux scores négatifs ; sans effet sur K08, dont le score
  MI est toujours positif) ; en mode quadrigrammes, pas de substitution des textes de contrôle.
