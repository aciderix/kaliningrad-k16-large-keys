# Bilan au 2026-10-03 — tout ce qui a été tenté pour déchiffrer la bouteille, et ce qu'il en reste

Ce document rassemble en un seul endroit l'état de la recherche après les cellules K01–K28. Détails, chiffres et
contrôles : `README.md` (tableau des cellules), `docs/02_synthese.md`, et `experiments/K*/RESULTS.md`.

## 1. Verdict

**La bouteille n'est pas déchiffrée.** Après 28 cellules d'expériences, chacune calibrée sur des contrôles plantés,
aucune lecture ne résiste. Le texte a la composition de lettres d'un allemand un peu déformé, mais leur **ordre est
détruit** (aucun lien entre voisines) et aucune clé d'aucune famille classique ne le rétablit. Deux explications
restent, et aucune ne donne de prise à la cryptanalyse :

1. **un texte de type allemand mélangé sans clé** (lettres brassées localement ou globalement), puis maquillé en
   « mots » — dans ce cas le message n'est **pas reconstituable de façon unique** (K22 : à l'échelle mesurée, des
   milliards de textes allemands cohérents sont aussi compatibles que le vrai) ;
2. **un pseudo-texte sans message** fabriqué « à l'allemande » (piste évoquée dès 2015 par S. Aleshnikov,
   université Kant : jeu d'enfants de l'époque soviétique).

Une transposition à clé d'une famille encore non couverte reste possible en principe, mais rien ne la désigne.

## 2. L'objet

- Trouvée en 2015 rue Lénine 64-66 à Baltiysk (ex-Pillau) lors de travaux, dans une bouteille brune soviétique
  bouchée à la cire ; **deux feuilles de cahier** roulées, serrées par de la feuille d'aluminium et du fil de cuivre.
  Seules deux photos 688 × 841 circulent. La bouteille a été brisée et jetée ; selon la presse, les feuilles devaient partir à Moscou.
- K26 : les lignes délavées visibles sous la page 2 sont la **page 1 vue par transparence** (feuille 2 posée sur la
  feuille 1) — il n'y a pas de texte caché ; le cryptogramme est complet : 25 lignes + « eimat ».
- Transcription v1 confirmée par une transcription indépendante (Corsair_nv, 2015) et par les longueurs de blocs
  publiées par Norbert : 979 lettres en 6 blocs (166, 169, 162, 169, 169, 144), chacun clos par une lettre soulignée
  et un point, puis « eimat » et une rangée de points.

## 3. Ce que l'on sait du texte (mesures)

| Propriété | Valeur | Cellule |
|---|---|---|
| liens entre lettres voisines | **aucun** (z = 0,5 ; une langue, même chiffrée par substitution, ≈ 37) — aussi avec les 34 signes distincts | K02, K18 |
| mots répétés | 182 formes sur 194 « mots » : jamais vu dans une vraie prose | K04 |
| espaces | posés **après coup**, par une règle sur les lettres voisines (coupure entre deux voyelles ou deux consonnes) | K10, K11 |
| apostrophes, « i » isolé, abréviations | 116 apostrophes toutes après consonne, abréviations sans voyelle : **habillage** « à la russe » | K02, K18 |
| alphabet | celui de l'allemand, lettre pour lettre (lettres absentes = j q x y, les plus rares de l'allemand) | K17 |
| décompte | le plus proche de l'allemand parmi 97 langues, mais **incompatible** : f 46 et w 36 (f + w = 82 contre 59 au plus en allemand), trop de n ; trop peu de a, b, c, g | K17, K25 |
| ordre local | faible reste d'ordre « allemand » à courte distance, **presque entièrement à l'intérieur des mots de l'habillage** | K19–K23 |
| signature de lettres inventées à la main | aucune (ni cyclage, ni suites alphabétiques) | K18 |

## 4. Ce qui est exclu (contrôles de puissance réussis)

| Famille | Portée | Cellules |
|---|---|---|
| lecture dans l'ordre, toute langue, toute substitution (y compris homophonique, cyrillique « déguisé ») | — | K02, K18 |
| même passage chiffré 7 fois ; mots du clair conservés (avec ou sans anagramme) | — | K01, K04 |
| Vigenère, Playfair, Bifid, homophonique, polyalphabétique | — | K12, K18 |
| routes (colonnes, zigzags, diagonales, spirales), barrière 2–100 rails, décimation | toutes largeurs, texte entier et blocs | K06, K09 |
| colonnes à clé, ± substitution | largeurs 5–40 | K03, K07 |
| double transposition en colonnes | toutes clés de 3 à 9 colonnes | K08 |
| double transposition, même clé (Übchi) | 10–15 colonnes | K14 |
| **double transposition à clés-mots** | **≈ 34 000 mots allemands, russes (ordre cyrillique ou latin), prénoms, noms de lieux, expressions ; toutes longueurs ; 16 variantes ; texte entier et par bloc** | **K27** |
| Myszkowski, AMSCO, nihiliste | 5–15 ; 3–12 ; blocs carrés | K13 |
| grilles tournantes (Fleissner, Verne) | 4×4 à 13×13 | K05, K19, K21 |
| grille de Cardan fixe commune aux blocs | 25–169 cases | K24 |
| permutations périodiques à clé fixe | période ≤ 25 avec nuls, ≤ 36 sans | K19 |
| transpositions ligne par ligne, lecture de la page en colonnes | — | K19, K28 |
| « eimat » / « Heimat » comme clé (colonnes, double, Vigenère, Beaufort, zigzag) | — | K28 |
| messages dans l'habillage (initiales, finales, apostrophes, abréviations, lettres soulignées) | — | K17, K18 |
| texte source connu brassé localement | 2 386 livres allemands de Gutenberg, 11 192 chants, Bibles Luther, Schlachter, synodale | K21 |
| « solutions » annoncées (T. Ernst 2017, « Frank » 2021, Bible synodale) | jamais publiées ; contredites par les mesures | K18 |

## 5. Ce qui reste ouvert

- Transpositions à clé **non tirée d'un mot** et à structure plus riche : double transposition à deux clés
  quelconques de 10 colonnes et plus (K16 : puissance insuffisante, mais K17 montre qu'un allemand ordinaire est de
  toute façon exclu ; il faudrait des nuls), grilles différentes pour chaque bloc, grilles tournantes à clé changeante.
- Mélange sans clé (local ou global) d'un texte allemand non standard : vérifiable si on propose un texte, jamais
  démontrable comme unique (K22).
- Pseudo-texte sans message.

## 6. Ce qui pourrait débloquer

1. **Les feuilles originales** (meilleures images, revers, traces de brouillon) : presse de 2015 — université Kant
   (S. Aleshnikov), musée de Baltiysk ; découvreur : le monteur E. Iaromtchouk.
2. La méthode annoncée par T. Ernst ou « Frank », si elle est publiée : elle se teste en quelques minutes contre les
   mesures K02, K12, K17, K18.
3. Une information extérieure sur le contenu (auteur, date, texte source).

## 7. Vérifier une proposition de solution

`python3 tools/k28/verifier.py proposition.txt` donne le bilan des lettres (nuls nécessaires, lettres impossibles),
le déplacement maximal qu'il faudrait admettre pour passer du clair proposé à la bouteille, et la même mesure sur
200 fenêtres d'allemand sans rapport : une vraie solution doit faire nettement mieux qu'un texte quelconque. Une
transposition proposée avec sa clé se vérifie exactement (même multiensemble de lettres, même ordre après
chiffrement).
