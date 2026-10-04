# K04 — Les mots du chiffré sont-ils les mots du clair ? (répétitions de mots, invariantes par substitution et anagramme) — PRÉ-INSCRIPTION

Rédigée avant le test formel (2026-09-28). Déjà vu en exploration (déclaré) : le chiffré a 184 multiensembles de lettres distincts
pour 194 mots ; les 9 abréviations ne contiennent aucune voyelle.

## Hypothèse testée (famille « mots conservés »)
Les espaces du chiffré sont ceux du clair, et chaque mot a été chiffré par une règle **fixe** lettre à lettre (substitution
simple, éventuellement avec variantes notées par apostrophes/accents fusionnées ici), avec ou sans **brouillage des lettres à
l'intérieur de chaque mot**. Cette famille expliquerait l'absence de contacts (K02) et les espaces réels (T6).
Prédiction : les mots répétés du clair (et, le, de, и, в, не…) restent des mots de même multiensemble de lettres.

## Statistique
D = nombre de multiensembles de lettres distincts parmi 194 mots consécutifs (variante A : lettres a-z, accents fusionnés,
apostrophes, points et soulignements ignorés ; jetons sans lettre supprimés). Invariante par toute substitution simple et tout
brouillage interne aux mots. Plus D est grand, moins il y a de répétitions.

## Référence
Fenêtres de 194 mots consécutifs (pas de 97 mots) dans des textes réels : allemand, néerlandais, anglais, français, italien,
espagnol, latin, espéranto (corpus déjà utilisés), et russe, polonais, tchèque, finnois, hongrois, suédois, danois (Gutenberg,
téléchargés pour ce test ; en-têtes Gutenberg retirés). Langues très flexionnelles et agglutinantes incluses exprès : ce sont
celles où D est le plus grand.

## Décision
Si D(chiffré) dépasse le maximum observé dans **toutes** les langues, la famille « mots conservés » est rejetée (pour ces langues
et, par extension raisonnable, pour les langues de même type). Contrôle positif : un texte allemand transposé (grille à clé de
K03) puis recoupé en faux mots avec les longueurs de mots du chiffré doit donner un D du même ordre que le chiffré.

## Portée
Ne dit rien des chiffres dont la règle change d'un mot à l'autre (mais K02/IC : de tels chiffres aplatiraient les fréquences, or
l'IC vaut 0,083).
