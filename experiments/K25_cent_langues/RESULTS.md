# K25 — Le décompte des lettres comparé à 97 langues (2026-10-03)

Statut : exploration calibrée. Outils : `tools/k25/langprofile.py`, `tools/k25/fetch_leipzig.sh` ; sorties :
`logs/lang.out`, liste des corpus `logs/corpora.txt`.

## Pourquoi
K18 n'avait comparé le décompte de la bouteille qu'à 11 langues. Kaliningrad est entourée de langues jamais testées
(lituanien, letton, polonais régional, bas-allemand, yiddish, langues scandinaves). On étend la comparaison à
**97 langues et dialectes** (corpus de phrases de l'université de Leipzig, 10 000 à 30 000 phrases chacun, surtout
Wikipédia 2021 ; 7 langues demandées n'existent pas dans ce format).

## Deux tests
1. **Décompte direct** (le message a seulement été transposé : les lettres sont celles du clair) : G lettre à lettre,
   accents repliés ; p = part des fenêtres de 979 lettres de la langue aussi éloignées. Langues à alphabet latin (81).
2. **Profil trié** (le message a été transposé **et** chaque lettre remplacée par une autre) : seules les fréquences
   triées subsistent (méthode de K18), toutes écritures comprises (cyrillique, grec, géorgien, hébreu, arabe…).

## Résultats
**Décompte direct.** Classement par distance G (plus petit = plus proche) : allemand 153, luxembourgeois 196,
bas-allemand 224, palatin 268, frison 271, alémanique 275, néerlandais 343, bavarois 348 … ; toutes les autres langues
au-delà de 350 (lituanien 1 204, letton 1 294, polonais 853, suédois 607, russe et yiddish hors alphabet latin).
**La bouteille reste plus proche de l'allemand que de toute autre langue**, sans être compatible avec lui
(p = 0,0025). Aucune langue n'atteint p = 0,05 ; les meilleurs p (bas-allemand 0,051, créole haïtien 0,049) viennent
de corpus hétérogènes (plusieurs orthographes, passages étrangers) qui élargissent la dispersion des fenêtres : le
créole haïtien, à G = 700, n'est évidemment pas un bon candidat. Les langues baltes et slaves sont exclues sans
substitution : elles demandent des j et des y (2 à 8 % des lettres), absents de la bouteille.

**Profil trié** (lecture fixée à l'avance : 22 lettres, accents repliés des deux côtés). **16 langues sur 97 sont
compatibles** (p > 0,05) : lombard (0,75), sicilien (0,55), ido, volapük, piémontais, ligure, silésien, suédois,
catalan, latin, judéo-espagnol, créole haïtien, bas-allemand, swahili, basque, võro. L'allemand (0,0035), le russe
(0,006 ; 0,06 avec la lecture « tous signes distincts »), le néerlandais, le polonais, le lituanien et le letton ne le
sont pas. Plusieurs de ces corpus sont hétérogènes (le lombard de Wikipédia mêle plusieurs orthographes), ce qui rend
le test indulgent.

## Lecture
1. Le profil trié est un indice faible : une langue sur six passe. **K18 est nuancé** : « aucune des 11 langues »
   était vrai, mais sous transposition + substitution, de nombreuses autres langues restent possibles ; le décompte
   seul ne peut ni identifier la langue d'un clair substitué, ni exclure cette famille.
2. Sans substitution, la bouteille est **plus proche de l'allemand et de ses voisins** (luxembourgeois, bas-allemand,
   dialectes du sud) que de toute autre langue, mais aucune n'est compatible : l'écart (trop de n, f, w ; trop peu de
   a, c, g, b, t) reste celui décrit en K12–K18. Aucune langue de la région (baltes, slaves, scandinaves, yiddish)
   n'explique mieux le décompte.
3. Rien de neuf ne permet de choisir entre « allemand transposé avec des nuls », « clair substitué puis transposé »
   et « pseudo-texte à l'allemande ».
