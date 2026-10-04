# K03 — Grille carrée à clé, section par section, notée en allemand — PRÉ-INSCRIPTION

Rédigée et commitée avant toute recherche de clé sur le texte (2026-09-28).

## Hypothèse testée (hypothèse A de K02, forme la plus simple)
Chaque section complète de taille carrée est un morceau de texte **allemand** écrit dans un carré et transposé par une clé
(permutation de colonnes ou de lignes), lettres inchangées. Sections : S2, S4, S5 (169 = 13²) et S6 (144 = 12²). S1 (166) et S3
(162) sont exclues (carré incomplet : disposition inconnue).

## Modèles (texte en lignes de q lettres, q = 13 ou 12 ; C = section chiffrée, découpée en q morceaux de q)
- **V1 (colonnes à clé)** : le morceau j est la colonne π(j) du carré ; le clair se lit en lignes.
- **V2 (opération inverse de V1)** : C[k·q + π(j)] = clair[j·q + k] (écriture en colonnes à clé, lecture en lignes).
  (Correction avant calcul : la « V2 lignes à clé, lecture en colonnes » écrite d'abord est identique à V1 sur un carré complet.
  La permutation de lignes lues en lignes conserverait les contacts dans chaque ligne : déjà exclue par K02.)
Pour chacun, on ajoute la lecture inversée du résultat (clair lu à l'envers) : 4 lectures au total, on garde la meilleure, **la
même règle s'appliquant aux contrôles et aux nuls**.

## Recherche et score
Score = moyenne des log-probabilités de quadrigrammes allemands (`dagapeyeff/data/models/qg_de.bin`, entraîné sur un corpus
distinct du texte réservé). Recherche : montée avec redémarrages (échanges, déplacements de blocs de π) ; l'effort (redémarrages,
itérations) est **fixé sur les contrôles** avant le texte réel puis gelé. Outil : `tools/k03_columnar.c`.

## Contrôles (avant le texte)
(a) Puissance : 20 blocs de 169 lettres et 20 de 144 du texte allemand réservé (`dagapeyeff/data/heldout/de.txt`), chacun chiffré
V1 ou V2 avec une clé aléatoire ; succès = ≥ 90 % des positions retrouvées. Exigé : ≥ 80 % de succès pour chaque taille, sinon
le test est déclaré sans puissance.
(b) Robustesse aux particularités de fréquence observées (K02 : excès de f, w) : mêmes blocs après remplacement aléatoire de 5 %
des lettres ; taux de succès rapporté (pas de seuil).
(c) Nul : pour chaque section réelle, 200 permutations aléatoires de ses lettres, même recherche ; score maximal obtenu.

## Décision
Une section « répond » si son meilleur score dépasse **tous** ses 200 nuls (p < 0,005 ; 4 sections ⇒ p global < 0,02). Toute
réponse est imprimée telle quelle. Aucune solution ne sera revendiquée sans texte allemand lisible et cohérent sur plusieurs
sections (oracle : lisibilité + cohérence des clés), jamais sur le seul score.

## Portée
Un résultat négatif n'exclut que les grilles carrées à clé simple (colonnes ou lignes) avec lettres inchangées et plaintext
allemand ; il laisse ouvertes les routes, doubles transpositions, grilles tournantes, substitutions combinées, et l'hypothèse B
(pseudo-texte).

## Amendement 1 (avant tout calcul sur le texte réel)
Premier essai des contrôles : le critère « ≥ 90 % des positions » compte comme échecs des résultats lisibles dont les lignes sont
décalées circulairement (ambiguïté propre à ces grilles). Nouveau critère de succès : **≥ 90 % des paires de lettres voisines du
résultat sont voisines dans le clair**. L'effort de recherche est ensuite fixé sur les contrôles (règle inchangée).
