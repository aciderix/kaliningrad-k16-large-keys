# K18 — Contre-expertise : sources, « solutions » annoncées, signes diacritiques, autres langues, lettres inventées (2026-10-03)

Statut : **exploration a posteriori** (non pré-inscrite), chaque test étant calibré sur des textes réels ou des
mélanges aléatoires. But : rouvrir toutes les pistes de lecture encore ouvertes après K17, avec un regard neuf.
Outils : `tools/k18/*.py` (corpus de référence non versé : `sh tools/k18/fetch_corpus.sh <dossier>`, puis
`K18_CORPUS=<dossier>`). Sorties : `logs/`.

**Résultat d'ensemble : aucun déchiffrement.** La bouteille n'est toujours pas résolue ; K18 ferme plusieurs
échappatoires et ajoute une observation nouvelle (§ 4).

## 1. Sources revues

- Photos : les deux images 688 × 841 de K. Schmeh (Cipherbrain, 2016/2017) ont été récupérées et examinées
  (agrandissements). Même résolution que pour la transcription v1 ; rien de plus n'y est lisible. Un « f » de
  `cfefdrr` paraît de forme un peu différente, mais la résolution ne permet pas d'affirmer deux glyphes distincts ;
  les deux transcripteurs indépendants lisent f partout.
- Les 72 commentaires des deux billets de Cipherbrain (14 + 58) ont été lus. Deux « solutions » y sont annoncées,
  **jamais publiées** :
  - Thomas Ernst (oct. 2017) : texte d'origine cyrillique, « politique », chiffre polyalphabétique dont la clé change
    à chaque lettre ; l'apostrophe vaudrait une lettre dépendant de la précédente ;
  - « Frank » (févr. 2021) : un chapitre de la Bible synodale russe (Filaret, 1876), « méthode assez compliquée ».
  Recherche web (2026-10-03, anglais et russe) : aucune publication de solution, ni de ces auteurs ni d'autres.
  Les lectures allemandes partielles d'A. Ulyanenkov (« neue Eilbote », « wurde Heimat ») supposent une lecture dans
  l'ordre.

## 2. Liens entre lettres voisines : revérifiés, aussi avec les signes comme symboles distincts

Information mutuelle à distance d (`contacts.py`, 400 mélanges) :

| Lecture | d = 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 22 lettres (accents repliés) | z = −0,1 | +0,3 | −1,3 | −2,6 | +0,1 |
| 34 symboles (n', t', ê, ö… distincts) | −0,6 | +0,7 | −1,5 | −0,3 | +0,9 |
| contrôle : allemand réel, 979 lettres | **+30,7** | | | | |

K02 est confirmé, y compris quand les apostrophes et accents sont des symboles à part entière. Conséquence : **toute
lecture dans l'ordre est exclue**, quelle que soit la substitution — y compris homophonique (si chaque symbole
désigne une seule lettre du clair, l'information entre voisins du clair est conservée), ou un « cyrillique déguisé »
par ressemblance de formes (n = п, m = т, u = и…). Les lectures d'Ulyanenkov sont donc incompatibles. Un
polyalphabétique détruirait les liens, mais il aplatit aussi les fréquences, ce que le flux ne montre pas (IC 0,083 ;
K12) : la piste de T. Ernst est défavorisée.

## 3. Profil trié (invariant par toute substitution) : 11 langues × 4 lectures des signes

Une transposition, éventuellement suivie d'une substitution lettre à lettre, conserve le profil trié des
fréquences. On compare celui de la bouteille aux fenêtres de 979 lettres de chaque langue (`t2multi.py`) ; p =
part des fenêtres réelles aussi éloignées.

| Langue (corpus) | 22 lettres | accents gardés (25) | apostrophes distinctes (31) | tout distinct (34) |
|---|---:|---:|---:|---:|
| allemand (21 livres) | p = 0,0003 | **0,011** | **0,008** | 0 |
| russe, Bible synodale | 0 | 0 | **0,008** | 0,0015 |
| néerlandais | 0 | 0,006 | 0 | 0 |
| finnois | 0,004 | 0,001 | 0 | 0 |
| anglais, espagnol, français, italien, portugais, latin, polonais | ≤ 0,0006 | ≤ 0,0006 | 0 | 0 |

Aucune langue n'est compatible sous une lecture fixée à l'avance ; les meilleurs cas sont à p ≈ 0,01.
**L'affirmation de « Frank » (Bible synodale)** suppose donc, si l'ordre a été mélangé, une transformation qui change
aussi fortement les fréquences : rien de tel n'est connu des chiffres manuels.

Observation (a posteriori) : sans les 41 n', il reste 95 n, exactement la proportion allemande (9,8 %). En rendant
distincts certains symboles apostrophés seulement (n' et t', par exemple), le profil trié devient parfaitement
allemand (G = 12–14, au niveau médian des fenêtres) ; mais 1 024 combinaisons ont été examinées (`t2rich2.py`) et
une sélection parmi autant de variantes fabrique ce résultat : **coïncidence non probante**.

## 4. Observation nouvelle : aucune signature de lettres inventées à la main

Une personne qui écrit des lettres « au hasard » laisse des traces bien connues : elle évite les répétitions
proches, fait revenir chaque lettre à intervalles trop réguliers (« cyclage ») et produit des suites alphabétiques.
Le flux (`repeats.py`, `human.py`, 3 000–4 000 mélanges) :

| Signature | Bouteille | Attendu (mélanges) | z |
|---|---:|---:|---:|
| lettres identiques à distance 1 | 68 | 81,3 | −1,6 (p = 0,06) |
| à distance 2 / 3 | 91 / 86 | 81,0 / 81,0 | +1,2 / +0,6 |
| distances 4 à 12 | — | — | entre −0,9 et +1,1 |
| dispersion des écarts entre occurrences (cyclage) | 0,863 | 0,884 ± 0,069 | −0,3 |
| paires alphabétiquement voisines | 94 | 83,7 ± 8,3 | +1,2 |

Même résultat sur la page 1 seule (−1,4 à distance 1) et sur la transcription indépendante de Corsair (−1,3). Le
léger déficit de doublets vient de l'habillage (K10 : on coupe entre deux lettres identiques). Le flux se comporte
comme **un mélange mécanique d'un stock fixe de lettres** : transposition d'un texte, ou tirage mécanique (lettres
découpées et tirées, par exemple). Cela défavorise la forme « manuelle » de l'hypothèse B (lettres écrites au fil
de la plume), sans exclure un tirage mécanique dans un stock fabriqué.

Les six blocs sont homogènes (`hetero.py` : χ² toutes lettres p = 0,77 ; f seul p = 0,17 ; 20 000 permutations).

## 5. Canaux cachés dans la mise en forme : aucun

`channels.py` : apostrophes lues comme bits sur les 640 consonnes (groupes de 5, 5 décalages), longueurs de mots
lues comme lettres, initiales et finales de lignes (`euuddeseeeurfdgdsieioataa`, `sfffskneaesgnfriunetiuesn`) :
rien de lisible. Les apostrophes sont plus fréquentes en fin de « mot » (27 % des consonnes finales contre 16 %
ailleurs) et viennent en grappes (`d't'`, `kt't'set'`, `n'n'`) : un effet d'habillage « à la russe » (-нь, -ть),
cohérent avec K10–K11, pas un code.

## 6. Allemand non standard ? (ajustements calibrés)

| Modèle | Bouteille | Même optimisation sur des fenêtres réelles | Lecture |
|---|---|---|---|
| allemand + nuls choisis parmi f, w, n (`nulls.py`) | corpus propre (11 livres, `K18_CLEAN=1`) : G 126 → 51 en retirant 32 f, 19 w, 48 n | 21/300 fenêtres allemandes aussi loin après la même optimisation (**p ≈ 0,07** ; 0,13 avec le corpus complet, pollué par des passages étrangers) | **seul modèle simple encore à la limite de la compatibilité**, avec 3 paramètres libres et aucun indice indépendant |
| 4 réécritures gloutonnes de digrammes ou lettres (`rewrite.py`, 35 motifs × 27 remplacements par étape) | `ei→f`, `sch→w`, `au→n`, `ng→n` : G 132 → 62 (p = 0,09) | la même recherche réduit l'écart d'autres langues d'environ 60 % (néerlandais 325 → 125, anglais 354 → 160 ; p ≤ 0,005) | règles sans motif linguistique (personne n'écrit « ei » avec un f) : **ajustement non interprétable** |

Seule `sch → w` aurait une justification (le ш cursif ressemble à un w), mais elle ne suffit pas. Aucune variante
dialectale, phonétique ou orthographique simple ne ramène le décompte à l'allemand.

## 7. Pistes examinées et écartées sans calcul lourd

- Spectre des liens à toutes les distances 1–599 (`spectrum.py`) : maximum z = 3,8 (d = 416) contre 3,7 au 95ᵉ
  centile du maximum des nuls ; marginal et a posteriori. Le contrôle (colonnes à clé de largeur 12) montre que ce test
  est peu sensible ; K07 couvre déjà ce cas.
- Anagramme multiple sur les trois blocs de 169 lettres (S2, S4, S5) sous une permutation commune quelconque : rejeté
  a priori. Avec trois messages, l'optimum obtenu sur des lettres au hasard (≈ 168 × 3,5 nats) dépasse le score d'une
  vraie remise en ordre (≈ 168 × 3 × 0,45 nats) : sans puissance (même leçon que K15-F).

## 8. Conclusion

1. **Non déchiffrée.** Aucune lecture, ni allemande ni russe, ne résiste aux contrôles. Les deux « solutions »
   annoncées sur Cipherbrain n'ont jamais été publiées et contredisent des propriétés mesurables (liens entre
   voisines absents, fréquences non aplaties, décompte incompatible avec la Bible synodale).
2. Ce que l'objet est le plus probablement : un **flux de 979 lettres mélangé mécaniquement** (aucune trace de
   lettres inventées à la main), dont le décompte n'est celui d'aucune des 11 langues testées, même sous substitution,
   **puis habillé en texte** par une main formée à l'écriture cyrillique (« i » isolé comme mot, apostrophes façon
   signe mou, tracé des lettres ; K10–K11).
3. Deux familles restent ouvertes, toutes deux sans prise cryptanalytique actuelle :
   - **A″** — transposition à clé complexe d'un clair non standard (par exemple de l'allemand avec ≈ 100 nuls f, w,
     n) ; il faudrait connaître l'orthographe du clair *et* une famille de clés structurée pour chercher la clé ;
   - **B mécanique** — tirage sans message dans un stock de lettres « à l'allemande » fabriqué par l'auteur.
4. Ce qui pourrait débloquer la question : les **feuilles originales** (la presse de 2015 parle de « plusieurs
   feuilles » ; seules deux photos circulent ; université Kant, S. Aleshnikov ; musée de Baltiysk), ou la méthode
   annoncée par « Frank » ou T. Ernst si elle est un jour publiée — elle pourrait alors être testée ici en quelques
   minutes contre les mesures de K02, K12, K17 et K18.
