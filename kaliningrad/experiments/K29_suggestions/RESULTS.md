# K29 — Examen de six suggestions externes (2026-10-03)

Statut : chaque affirmation vérifiable a été confrontée aux résultats existants ou testée, avec contrôles. Outils :
`tools/k29/` ; sorties : `logs/`. Les suggestions (texte reçu le 2026-10-03, auteur non précisé) sont résumées en tête de
chaque section.

## 1. « Le paradoxe de K23 » : l'ordre local a été injecté à la fabrication des mots

> Le signal de bigrammes est à +3,0 dans les « mots » et +0,1 entre eux ; un texte brassé puis découpé aurait dû
> laisser déborder le signal ; donc l'ordre local vient de la fabrication des mots.

**D'accord sur le fond : c'est la conclusion de K23.** Deux nuances : ce n'est pas une impossibilité mathématique mais
un écart statistique (un seul test, quatre contrôles par cas, dispersion importante) ; et le complément de K23 trouve,
entre les mots, aux distances 5–40, une trace faible (z = +2,2, p ≈ 0,016), à peine plus compatible avec un brassage
local qu'avec un mélange complet. Rien de nouveau à tester.

## 2. L'excès de f, w, n

### 2A. F = *Füllbuchstabe*, W = *Worttrenner*, N = *Null*
- **W séparateur de mots : exclu.** Un allemand de 979 lettres compte ≈ 190 mots (Kafka) : w vaudrait ≈ 207, contre
  36 (`logs/decompte.out`). W séparateur de **phrases** (≈ 7 par 979 lettres) donnerait w ≈ 23 : n'explique qu'une
  partie de l'excès.
- F et N comme nuls : c'est exactement le modèle « allemand + nuls f, w, n » de K18, le seul encore à la limite
  (p ≈ 0,07). L'étiquette « Füllbuchstabe / Null » n'ajoute pas de prédiction testable. À noter : les procédures
  allemandes connues (militaires notamment) utilisaient X comme séparateur ; la bouteille n'a **aucun** x, q, j, y.

### 2B. Nombres écrits en toutes lettres
Mélange allemand + proportion α de nombres en toutes lettres, α ajusté (0 à 100 %), fenêtres de référence construites
de la même façon (`tools/k29/decompte.py`, corpus « propre » de K18) :

| Genre de nombres | f, w, n, g dans ces nombres | meilleur α | p |
|---|---|---:|---:|
| (aucun : allemand transposé, K17) | | — | 0,0012 |
| cardinaux 1–100 | f 3,4 %, w 1,7 %, n 14,1 %, **g 6,6 %** | 0,02 | 0,0012 |
| chiffres « à la militaire » (eins, zwo, … null) | f 4,8 %, w 2,3 %, n 14,3 %, g 0 | 0,20 | 0,0019 |
| années et dates | f 2,4 %, w 1,9 %, n 17,6 %, g 2,8 % | 0,20 | 0,0015 |

**Non.** Les nombres augmentent n, mais pas assez f et w ; les cardinaux ajoutent des g (-zig), alors que la bouteille
en manque. Aucun mélange ne rend le décompte compatible.

### 2C. « sch » écrit w (ш cursif)
`sch` ne fait que 7,8 occurrences pour 979 lettres d'allemand : la règle pourrait expliquer au plus 8 des ≈ 20 w en
trop et 8 des ≈ 15 c manquants, et rien pour f. Mesuré : p passe de 0,0012 à 0,0020 ; avec ê = ä en plus, 0,0024.
**Insuffisant** (déjà noté en K18).

## 3. Les carrés 13×13 et 12×12

> Les blocs sont des grilles 13×13 (169) et 12×12 (144) ; les solveurs à quadrigrammes échouent à 100 % avec 10 % de
> nuls ; la méthode siamoise de La Loubère n'a pas été testée.

- **« Les quadrigrammes échouent à 100 % avec des nuls » : inexact.** Les contrôles de K19, K21, K27 et ceux
  ci-dessous contiennent 10 % de nuls f/w/n et sont retrouvés. **Mais le point est juste pour les grilles tournantes
  à clé différente par bloc** (K05 l'avait signalé : puissance divisée par deux avec 5 % de lettres altérées).
  Mesuré ici avec 10 % de lettres altérées : clé retrouvée **2/12** (13×13) et **4/12** (12×12), et la meilleure note
  trouvée est souvent supérieure à celle du vrai clair (`logs/fleissner_ctrl_*`). Sur 169 lettres avec 10 % de bruit,
  la note de quadrigrammes ne suffit pas à trancher : **cette famille (grille tournante, une clé par bloc, avec nuls)
  n'est pas testable avec les outils actuels.** La même grille pour tous les blocs reste exclue, nuls compris (K21).
- **La Loubère et toutes les marches régulières : testées, exclues** (`tools/k29/affine.c`). Famille exhaustive :
  toutes les marches **affines** du tore 13×13 (la k-ième lettre, k = 13q + r, va dans la case
  (r₀ + a·r + b·q, c₀ + c·r + d·q) mod 13, matrice inversible). Cela fait 26 208 matrices × 169 départs × 2 sens, soit
  8,86 millions de marches. Elle contient la méthode siamoise de La Loubère et ses symétries, Bachet et de la Hire à
  pas uniformes, les lignes, colonnes, diagonales et sauts de cavalier. Même chose mod 12 pour le bloc de 144
  (1,33 million), plus le carré magique doublement pair classique. Blocs incomplets (166, 162) : cases vides sautées.

| | clé commune S1–S5 | meilleur bloc seul (S1 … S6) |
|---|---:|---|
| contrôles (allemand + 10 % de nuls ; La Loubère, marche quelconque) | **−10,59 ; −11,06**, clé exacte | **−10,0 à −11,7**, les 12 blocs retrouvés |
| bouteille (`logs/affine_bouteille.out`) | −14,80 | −14,48 ; −14,04 ; −13,25 ; −13,66 ; −13,87 ; −13,57 |
| bouteille mélangée, 3 tirages (`logs/affine_melanges.out`) | −14,80 à −14,88 | −13,2 à −14,4 |

La bouteille est exactement au niveau de ses propres lettres mélangées.
- **Carreaux de 5 mm : non.** Les feuilles sont **réglées** (lignes horizontales tous les ≈ 35 px, soit ≈ 8,5 mm ;
  aucune ligne verticale sur l'agrandissement de la page 2) : rien n'imposait des carrés de 13 cases.

## 4. Apostrophes = signe mou ь ; mots russes (« gon'it' »)

`tools/k29/russe.py`, `logs/russe.out` (liste de fréquence russe de 50 000 formes, six translittérations).

| consonne + apostrophe | n | t | r | d | s | f | l | m | z | ш |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bouteille (118) | **36 %** | 25 % | 11 % | 10 % | 5 % | 5 % | 4 % | 3 % | 2 % | 0 |
| russe : consonne suivie de ь | 7 % | **40 %** | 3 % | 2 % | 12 % | 0 % | **18 %** | 1 % | 1 % | 12 % |

- **Les apostrophes ne suivent pas le signe mou.** En russe, ь suit d'abord t, l, s, ш ; dans la bouteille, n domine,
  l est rare, ш absent, et 6 f' n'ont pas d'équivalent russe. Un modèle « ь russe » est moins vraisemblable, de
  **80 unités log**, qu'un placement des apostrophes au hasard sur les consonnes de la bouteille. Fréquence :
  12 % des lettres portent une apostrophe, contre 2,3 % de ь en russe.
- **Mots russes : au niveau du hasard.** Mots de la bouteille présents dans le lexique russe translittéré : 17
  (≥ 2 lettres), 2 (≥ 4), 1 (≥ 5 : `gonit'`). Pour 500 bouteilles témoins (mêmes longueurs de mots et apostrophes,
  lettres mélangées) : 14,1 ± 3,0 ; 1,1 ± 1,1 ; 0,1 ± 0,4 (p = 0,21 ; 0,31 ; 0,11). Un lexique allemand donne
  autant (17 ; 2 ; 2, dont `rande` et `es'tes`, ce dernier venant du bruit de la liste). `gon'it'` (lecture de
  Corsair ; v1 lit `gonit'`) est **un mot russe que le hasard produit** à ce rythme. De plus, une lecture en russe dans
  l'ordre est exclue par l'absence de liens entre voisines (K02, K18) et par le o : 11 % des lettres russes, 1,2 %
  dans la bouteille (1,9 % avec ö).

## 5. ê (17 occurrences)

- ê = э russe : э fait 0,8 % des lettres russes (≈ 8 pour 979), contre 17 ê ; et le reste du décompte exclut le russe.
- ê = ä allemand : ≥ 17 ä n'arrive que dans **0,03 %** des fenêtres allemandes (moyenne 5,2). Replier ê sur a au lieu
  de e (ä est replié sur a dans le corpus) comble le déficit de a mais ne change presque rien au total (p 0,0012 →
  0,0015).
- Les deux ê isolés comme « mots » ne désignent pas une conjonction : э seul n'est en russe qu'une interjection rare ;
  ils sont du même ordre que le « i » isolé de l'habillage (K02, K10).
ê reste inexpliqué ; c'est plutôt une marque d'habillage (comme les apostrophes) qu'une lettre d'un clair connu.

## 6. Une « caisse de lettres » (касса букв) ou un tirage mécanique

(Le texte reçu s'arrête au milieu de cette section.) L'idée — un flux tiré mécaniquement d'un stock de lettres aux
proportions « allemandes », puis arrangé en mots prononçables — est **compatible** avec K18 (pas de signature d'une
main qui invente), K12 (blocs homogènes), K10–K11 (espaces posés après coup) et K23 (ordre local seulement dans les
mots). Elle ne fait pas de prédiction testable sans connaître la composition du stock : un jeu de lettres réel
(caisse scolaire, tampons d'imprimerie d'enfant) dont les proportions donneraient ≈ 4,7 % de f et 3,7 % de w serait la
seule pièce décisive. C'est la variante mécanique de l'hypothèse B (pseudo-texte), déjà retenue en K18–K23.

## Bilan

| Suggestion | Verdict |
|---|---|
| 1. ordre local injecté dans les mots | déjà la conclusion de K23 (avec ses réserves) |
| 2A. F/W/N = remplissage, séparateur, nul | W séparateur de mots exclu ; reste le modèle « nuls f, w, n » de K18 (p ≈ 0,07) |
| 2B. nombres en toutes lettres | exclu (p ≤ 0,002 ; les g vont dans le mauvais sens) |
| 2C. sch → w (ш) | insuffisant (8 sur ≈ 20 w ; f inexpliqué) |
| 3. La Loubère, marches régulières 13×13 / 12×12 | **exclu**, 8,9 M + 1,3 M marches, contrôles avec nuls 12/12 |
| 3. grilles tournantes par bloc avec nuls | **point juste : non testable** (puissance 2/12 à 4/12) |
| 3. carreaux de 5 mm | non : feuilles réglées en lignes |
| 4. apostrophes = ь ; mots russes | exclu (−80 unités log ; mots russes au niveau du hasard) |
| 5. ê = э ou ä | ni l'un ni l'autre (trop nombreux) |
| 6. tirage mécanique d'un stock de lettres | compatible, non testable sans le stock |
