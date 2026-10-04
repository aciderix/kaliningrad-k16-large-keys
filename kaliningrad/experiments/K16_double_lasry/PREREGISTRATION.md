# K16 — Double transposition à deux clés longues (10–20) — attaque Lasry / divide-and-conquer

Date : 2026-09-29.

## Question

Tester la famille qui reste hors de portée de K08/K14 : double transposition en colonnes, avec deux clés distinctes, largeurs w1,w2 = 10..20, texte entier de 979 lettres.

Modèle : P -> transposition colonne clé K1 (w1) -> T -> transposition colonne clé K2 (w2) -> C.

La bouteille n'est interprétée qu'après validation indépendante de la puissance de la recherche.

## Solveur

Outil : `tools/k16_double_ct2.c`.

Il reprend en C la méthode « divide-and-conquer » de Lasry, Kopal & Wacker :
1. recherche de K2 par potentiel de juxtaposition de colonnes (IDP), avec bornes exactes des colonnes et chaîne de voisinage ;
2. inversion de K2 ;
3. recherche de K1 par score quadrigramme allemand ;
4. criblage des paires (w1,w2) par IDP normalisé contre des clés aléatoires de même largeur, puis recherche profonde sur les meilleures paires.

Référence d'implémentation : CrypTool 2, `CrypPlugins/IDPAttack/IDPAnalyser.cs`.

## Contrôles

10 textes allemands réservés, 979 lettres, doublement transposés avec :
- w1,w2 tirés uniformément dans 10..20 ;
- clés aléatoires ;
- largeurs inconnues au solveur.

Succès d'un contrôle : >= 90 % des 978 voisinages du clair doivent être correctement recollés.

Critère de puissance : >= 8/10 pour la recherche complète inconnue.
Si < 8/10 : K16 est déclaré **sans puissance** et aucun résultat réel n'est interprété.

Un second lot de contrôles pourra être lancé aux deux largeurs difficiles identifiées lors du premier passage (notamment 13/17) avec effort augmenté, mais l'effort finalement retenu doit être gelé avant le texte réel.

## Recherche

Portée de criblage : toutes les 121 paires (10..20)^2.

Mode rapide : K16_SCREEN=Rs,Is,top.
Mode profond : R2,I2 pour les paires retenues.

Le criblage doit être évalué par z-score de l'IDP contre 40 clés aléatoires de même paire de largeurs afin de limiter le biais en faveur des grandes clés.

## Décision sur la bouteille

Après puissance >= 8/10 :
- seuil de langue : score quadrigramme >= -10.5 ;
- le meilleur réel doit dépasser les nuls prévus ;
- un résultat n'est considéré comme solution que si le texte récupéré est lisible et cohérent.

Si le seuil de langue n'est pas atteint, la famille est exclue dans cette portée, sous réserve que la puissance soit démontrée.

## Nuls

20 permutations aléatoires indépendantes des 979 lettres, même pipeline et mêmes paramètres que le réel.

Important : la bouteille ne doit jamais servir à sélectionner une paire de largeurs, un score, une graine ou des réglages avant le calcul des nuls.
