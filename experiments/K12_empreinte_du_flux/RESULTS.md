# K12 — RÉSULTATS (2026-09-29) : le flux n'est compatible qu'avec **une transposition (± substitution)** ou **une chaîne tirée lettre à lettre**

Pré-inscription : `PREREGISTRATION.md` (commit 0a680c2) + amendement 1 (1 000 échantillons par famille, avant le texte réel).
Outil : `tools/k12_empreinte.py` ; sorties : `logs/`.

## 1. Contrôles (1 000 échantillons par famille ; 40 échantillons supplémentaires pour juger)
Auto-compatibilité : F1 1,00 ; F2 0,97 ; F3 0,95 ; F4 0,97 ; F5 0,97 ; F6 0,97 ; **F7 0,88** (35/40, un échantillon sous le seuil de
0,90 : limite notée) ; F8 0,97 ; F9 0,93 ; F10 0,90. Clair/substitution, Vigenère, Playfair, Bifid et homophonique sont
**parfaitement séparés** entre eux et des autres (0,00 hors diagonale). Comme annoncé, transposition, transposition + substitution
et chaînes i.i.d. se recouvrent (0,68-1,00).

## 2. Bouteille (979 lettres)
Empreinte : IC 0,0832 ; MI(1) excès 0,0025 ; MI(2) 0,0020 ; IC périodique max 0,0846 ; pair/impair χ² 30,1 ; doublets alignés 34 ;
**22 lettres distinctes** ; excès de trigrammes répétés 28,8.
| Famille | Verdict | Statistiques hors intervalle (centile) |
|---|---|---|
| F1 clair | exclue | MI1 (0), MI2 (0), trigrammes (0) |
| F2 substitution simple | exclue | MI1 (0), MI2 (0), trigrammes (0) |
| F3 Vigenère (clé 3-12) | exclue | IC (100), MI1 (0), nb de lettres (0), trigrammes (0) |
| **F4 transposition** | **compatible** | — |
| **F5 substitution + transposition** | **compatible** | — |
| F6 Playfair | exclue | IC, MI1, MI2, IC périodique, doublets alignés (100), nb de lettres, trigrammes |
| F7 Bifid (période 5-10) | exclue | IC (100), IC périodique (100), nb de lettres (0) |
| F8 homophonique | exclue | IC (100), MI1, MI2, IC périodique, nb de lettres, trigrammes |
| **F9 chaîne i.i.d., fréquences allemandes** | **compatible** | — |
| **F10 chaîne i.i.d., fréquences de la bouteille** | **compatible** | — |

## 3. Conclusion (RÉSULTAT)
- **Dans les familles, paramètres et implémentations pré-inscrits de K12**, les statistiques utilisées excluent comme générateurs du flux : texte clair, substitution simple, Vigenère (et polyalphabétiques périodiques de ce
  type), Playfair, Bifid, substitution homophonique. Les raisons sont nettes : l'IC du flux est celui d'une langue (0,083), trop
  élevé pour les chiffres qui aplatissent les fréquences ; et il n'a aucun contact, contrairement aux chiffres qui les gardent.
- Restent **compatibles**, sans pouvoir être séparés par une empreinte statistique (limite annoncée d'avance) : une **transposition**
  d'un texte (avec ou sans substitution), ou une **chaîne produite lettre à lettre** sans enchaînement. Les procédés de transposition
  simples ou à clé courte sont déjà exclus un par un (K03, K05-K09).
- Le flux n'utilise que **22 lettres** (aucun j, q, x, y) : banal pour de l'allemand transposé (j, q, x, y y sont rares) ; à garder
  pour la suite.

## 4. Compléments (après discussion, explorations déclarées)
- Portée : l'exclusion vaut pour les implémentations testées (Vigenère clé 3-12, Playfair standard, Bifid période 5-10, homophonique
  à 26 symboles…), pas automatiquement pour toutes les variantes historiques de ces familles.
- Bifid (auto-compatibilité 0,88) : l'exclusion ne dépend pas de ce contrôle limite — IC de la bouteille 0,0832 contre 0,0480 ± 0,0041
  pour Bifid (maximum 0,066 sur 1 000 échantillons), soit 8,5 écarts-types au-dessus.
- « Un seul texte transposé puis découpé » contre « six segments transposés séparément » : **non décidable par la composition des
  blocs** — puissance mesurée 2 % (χ² d'homogénéité : 6 morceaux contigus d'allemand, moyenne 99,4 ; découpage aléatoire, 109,1 ;
  bouteille 94,6).
