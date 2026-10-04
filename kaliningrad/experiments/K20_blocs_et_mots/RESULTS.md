# K20 — Blocs ou texte entier ? Y a-t-il des mots allemands dans le brassage ? (2026-10-03)

Statut : **exploration** (non pré-inscrite), calibrée par des mélanges de la bouteille et par des contrôles
(allemand + 10 % de nuls f/w/n, brassé de différentes façons). Outils : `tools/k20/` (bibliothèques `tools/k18/`,
`tools/k19/` ; corpus `K18_CORPUS`) ; sorties : `logs/`.

## 1. Blocs ou texte entier ?

Question : les six sections (166, 169, 162, 169, 169, 144 lettres, chacune close par une lettre soulignée et un
point) sont-elles des unités de chiffrement, ou faut-il traiter le flux de 979 lettres d'un seul tenant ?

| Indice | Résultat | Source |
|---|---|---|
| composition des sections | homogène (χ² p = 0,77) ; « un texte découpé » et « six segments » indiscernables | K12, K18 |
| même clé pour les six sections (routes, colonnes, Übchi, grille tournante) | exclu (contrôles 7–10/10) | K15 |
| découpe régulière du brassage local (tailles 10–44) | aucune | K19 § 3.10 |
| signal local **à cheval** sur les 5 frontières de sections (`sections.py`) | z = +0,7, comme à des frontières tirées au hasard (+0,4 ± 0,9 ; rang 0,61) | K20 |
| lettres soulignées `epennn` (`underlined.py`) | 5 sur 6 sont e ou n ; mais les fins de « mots » de l'habillage le sont déjà à 40 % : p = 0,04, remarqué a posteriori | K20 |

**Réponse : le texte entier.** Rien n'indique que les sections soient des unités du chiffre : le brassage local les
traverse comme n'importe quel autre endroit (puissance faible : 5 frontières seulement). Elles ressemblent à un
découpage de présentation (longueurs voisines, 169 = 13², 144 = 12²) ou à des fins de phrases du clair (lettres
finales e/n, indice faible). Toutes les cellules travaillent donc sur le flux continu de 979 lettres ; les tests
« par bloc » (K03, K05, K13, K15) l'ont été en plus, et sont négatifs.

## 2. Les mots allemands sont-ils présents, en vrac, dans des fenêtres courtes ? (`wordspot.py`, `wordspot_file.py`)

Test : pour chacun des 6 000 mots allemands les plus fréquents (4 à 9 lettres), compter les fenêtres de longueur
« mot + k » qui contiennent toutes ses lettres ; somme des écarts réduits, comparée à 100–200 mélanges de la bouteille.

| Flux | k = 0 | k = 2 | k = 5 | k = 10 |
|---|---:|---:|---:|---:|
| **bouteille** | +0,24 | +1,23 | **+1,17** (p = 0,12) | +1,13 |

Puissance (k = 5, allemand + 10 % de nuls, 120 mélanges) : brassé par tranches de 20 lettres **+4,2 ; +4,6** ; de 40
lettres **+2,1 ; +2,2** ; de 80 lettres +1,0 ; +0,9 ; mélange global entre −0,3 et +0,8 (un tirage à +2,6 avec
seulement 40 mélanges : test bruité).

Les « mots trouvés » individuellement (kleider, gasthaus, rathaus…) sont ceux que le hasard produit quand on interroge
6 000 mots ; ils ne constituent **pas** une lecture.

Même test avec le vocabulaire d'autres langues (`wordlang.py`, 3 000 mots chacune) : bas-allemand +1,55, poésie
allemande +1,46, allemand +1,16, néerlandais +0,97, allemand de Pennsylvanie +0,93, russe translittéré +0,72,
anglais, polonais, espagnol, finnois +0,5 à +0,6, italien, français, portugais, latin ≈ 0 ou négatif. Classement
« germanique », comme au niveau des lettres (K19 § 3.8), mais **aucun score significatif** (p ≥ 0,07).

## 3. Deux mesures côte à côte (`twoaxes.py`)

| Flux | signal de paires de lettres (z, d = 1–10) | signal de mots (Z, k = 5) |
|---|---:|---:|
| **bouteille** | **+3,1** | **+1,2** |
| allemand brassé par 20 | +3,1 à +4,2 | +4,2 à +5,2 |
| allemand brassé par 40 | +1,9 à +3,2 | +2,1 à +5,8 |
| allemand brassé par 80 | −0,1 à +2,7 | +0,9 à +1,2 |
| allemand mélangé globalement | −1,0 à +0,3 | −0,3 à +2,6 |

La bouteille a des **paires de lettres** comparables à un allemand brassé par 20–40 lettres, mais un repérage de mots
plus faible que ces contrôles (écart d'environ 1 à 2 écarts-types, dispersion importante).

**Contrôle décisif sur le test lui-même** (`pseudo_gen.py`, `logs/pseudo.out`) : du **pseudo-allemand sans aucun vrai
mot** (chaînes de Markov de lettres d'ordre 1 et 2 apprises sur l'allemand), + 10 % de nuls, brassé par tranches de
20, obtient au repérage de mots **+2,2 à +5,7** (paires +2,8 à +4,8), autant que du vrai allemand. Le repérage de
mots ne distingue donc **pas** de vrais mots d'une simple statistique de lettres « à l'allemande » : il mesure des
co-occurrences locales de trois lettres ou plus. Le score plus faible de la bouteille dit seulement que cette
structure à plusieurs lettres y est plus faible que dans un brassage par 20 (brassage plus large ou plus bruité) ;
il ne dit **pas** si le texte brassé contenait de vrais mots.

## 4. Le signal a-t-il un sens de lecture ? (`asym.py`)

Un message laissé **dans l'ordre** mais entrecoupé de lettres de remplissage (grille de Cardan fixe, bourrage)
produit un signal orienté (paires « avant » plus allemandes que « arrière ») ; un brassage local, non.
Bouteille : asymétrie z = **+0,1** (distances 1–8), score avant +2,1. Contrôles : message à 60 % ou 40 % des lettres
+2,6 à +4,3 ; à 25 % +1,0 à +2,0 ; anagramme par tranches de 20 −0,7 à +1,8.
Le bourrage d'un message dans l'ordre est **défavorisé** (sauf si le message ne formait qu'environ un quart des
lettres) ; le brassage local reste compatible.

## 5. Conclusion

1. **On travaille sur le texte entier** : les sections ne se comportent pas comme des unités de chiffrement.
2. Le reste d'ordre local (K19) est **robuste au niveau des paires de lettres**, sans orientation, de type germanique.
3. Au niveau des **mots**, rien n'est démontré, dans un sens comme dans l'autre : le repérage de mots donne Z ≈ +1,2,
   en dessous des contrôles brassés par 20–40, mais ce test réagit aussi bien à du pseudo-allemand sans mots réels
   (§ 3). On ne peut donc trancher ni « vrais mots allemands » ni « pseudo-allemand ». La structure à plusieurs lettres
   est plus faible que pour un brassage par 20 : brassage plus large (≈ 40–80 lettres) ou plus irrégulier. K19 § 5
   est nuancé en conséquence : « tranches d'une vingtaine de lettres » vaut pour les paires de lettres.
4. Aucune lecture n'émerge ; les fragments de mots repérés relèvent du hasard.
