# Bouteille de Kaliningrad (Baltiysk, 2015) — recherche cryptanalytique

Même protocole que `dagapeyeff/docs/PROTOCOLE.md`. Choix de la cible : `docs/00_choix.md`.

- [`data/transcription_v1.txt`](data/transcription_v1.txt) — transcription de référence (26 lignes), faite ici d'après les photos de
  K. Schmeh, puis confrontée à la transcription indépendante de Corsair_nv (d3.ru, 2015 ; copie :
  `data/transcription_corsair_2015.txt`, à qui il manque une ligne). Détails : `docs/01_transcription_v1.md`. Contre-épreuve :
  les longueurs de sections entre lettres soulignées (166, 169, 162, 169, 169, 144, 5) sont identiques à celles de Norbert (2017).
  `transcription_v0.txt` = première version (glyphe r en forme de « 2 » noté x), conservée pour traçabilité.
- [`experiments/`](experiments/) — une cellule par dossier, pré-inscription commitée avant le résultat.

| Cellule | Question | Résultat |
|---|---|---|
| K01 structure | même passage transposé 7 fois ? même passage sous 7 substitutions ? mots allemands anagrammés ? | **les trois rejetées** (contrôles réussis) ; sections homogènes comme des morceaux d'un même texte (voir K02 pour la nature du texte) |
| K02 contacts | les lettres voisines sont-elles liées (toute langue) ? grille lue en colonnes ? espaces réels ? | **aucun contact** (z = 0,5 contre 37 pour une langue même substituée) ⇒ langue naturelle + substitution exclue ; pas de grille sans clé ; espaces liés aux lettres (« i » isolé, n/t finaux) |
| K03 grille à clé | les sections carrées (169 = 13², 144 = 12²) sont-elles de l'allemand transposé par une grille à clé ? | **non** (contrôles 95-100 % de réussite, même avec 5 % de lettres altérées ; réel p = 0,14 à 0,73 contre 200 nuls) |
| K04 répétitions de mots | les mots du chiffré sont-ils ceux du clair (toute substitution, avec ou sans anagramme) ? | **non** : 182 formes distinctes sur 194 mots, jamais atteint dans 13 langues en prose (russe, polonais, finnois… compris) ; espaces posés après coup sur des lettres mélangées |
| K06 routes | colonnes, zigzags, diagonales, spirales, toutes largeurs, par section et texte entier ? | **non** (contrôles 29/30 ; aucune suite crédible, meilleur score −13,7 contre −9 pour de l'allemand) |
| K05 grille tournante | blocs carrés = allemand sous grille de Fleissner ? | **non** (contrôles 19/20 et 17/20 ; réel au niveau des nuls, p ≥ 0,14) |
| K07 transposition sans langue | même question avec un score insensible à la substitution et à la langue (texte entier) | **non** pour les routes et les colonnes à clé 5-40 (MI réel 0,38-0,44 = nuls ; une vraie remise en ordre ≈ 0,9-1,1) ; blocs : sans puissance |
| K08 double transposition | Würfel (deux clés de colonnes 3-9), avec ou sans substitution, toute langue ? | **non** (contrôles 8/10 ; MI réel 0,408 = nuls ; clés ≥ 10 colonnes : hors de portée, déclaré) |
| K09 transpositions simples | barrière (2-100 rails) ou décimation, blocs et texte entier (+ substitution sur le texte entier) ? | **non** (contrôles 10/10 ; réel au niveau des nuls, textes illisibles) |
| **K10 habillage** (exploration contrôlée) | les espaces viennent-ils du clair, ou ont-ils été posés après coup ? | **posés après coup en regardant les lettres voisines** : frontières consonne\|voyelle 50 au lieu de 88 (z = −6,0 ; transcription indépendante −6,5 ; 488 fenêtres de 9 langues réelles : jamais sous −2,8) ⇒ un flux de lettres existant a été maquillé en « mots » |
| **K11 règle des espaces** (pré-inscrit) | quelle règle place les espaces ? | **coupure quand deux voyelles ou deux consonnes se rencontrent**, croissante avec la longueur du mot (p = 0,001 sur v1 et sur Corsair ; contrôles plantés 10/10, faux positifs 0/10, textes réels 40/40 au niveau du nul) ; l'identité des lettres n'aide pas (−9 contre +70 à +115 dans les vraies langues) |
| K12 empreinte du flux | à quelles familles de chiffres le flux de 979 lettres ressemble-t-il ? | **seulement transposition (± substitution) ou chaîne tirée lettre à lettre** ; exclus : clair, substitution, Vigenère, Playfair, Bifid, homophonique (contrôles : familles parfaitement séparées) |
| K13 transpositions restantes | nihiliste (blocs), Myszkowski (5-15), AMSCO (3-12), ± substitution ? | **non** (contrôles 8-10/10 ; aucun résultat n'approche un niveau de langue) |
| K14 double transposition, grandes clés | Übchi (même clé 10-15) ; deux clés différentes 10-20 ? | Übchi **non** (contrôles 9/10, réel = nuls) ; deux clés différentes longues : **hors de portée** (sans puissance, non interprété) |
| K15 blocs à clé commune | même clé pour les 6 blocs (routes, colonnes, Übchi, grille tournante), scores additionnés, ± substitution ? | **non** (contrôles 7-10/10 ; un score apparemment élevé — grille tournante MI 0,84 — égalé par les lettres mélangées) ; colonnes+substitution et double par bloc : sans puissance |
| K16 double transposition, clés 10–20 | double transposition allemande à deux permutations différentes ? | **aucun clair retrouvé** ; la recherche GitHub 15–20 a examiné les 36 paires en environ 6 minutes, mais les contrôles de puissance ne réussissent que 3/10 : résultat négatif non concluant |
| **K17 profil invariant** (≈ 1 s, sans clé) | le décompte des lettres peut-il être celui d'un texte allemand transposé ? | **non, quelle que soit la clé** : f + w = 82 contre 59 au plus dans 3 259 fenêtres allemandes ; décompte hors de toutes les fenêtres ; pas de substitution (lettres absentes = j q x y, identité 0/100 000). Les recherches K16 ne pouvaient pas aboutir |
| **K18 contre-expertise** (2026-10-03, exploration calibrée) | photos, « solutions » annoncées (T. Ernst 2017, « Frank » 2021 : Bible synodale), signes comme symboles distincts, 11 langues, lettres inventées à la main ? | **aucun déchiffrement** ; aucun lien entre voisines même avec 34 symboles (lecture dans l'ordre exclue) ; profil trié incompatible avec les 11 langues (p ≤ 0,011), Bible synodale comprise ; **aucune signature de lettres inventées à la main** (ni cyclage ni suites alphabétiques) ⇒ flux mélangé mécaniquement ; seul « allemand + ≈ 100 nuls f/w/n » reste à la limite (p ≈ 0,07) |
| **K19 mélange local** (2026-10-03, exploration calibrée) | chiffres « d'écolier » (groupes permutés, grille de Verne 4×4–7×7 exhaustive, transpositions par ligne) ? les lettres sont-elles mélangées sur tout le texte ? | **aucun déchiffrement** ; ces chiffres à clé fixe sont exclus (contrôles 3/3) ; **reste d'ordre à courte distance** mesuré de six façons (bigrammes z = +3,1, c près de h/k p = 0,008, anagrammes par ligne z ≈ +3, déplacements ≤ 3 z = +5,3), reproduit sur la transcription indépendante : un texte de type allemand **brassé par tranches d'une vingtaine de lettres**, sans clé ; un tel anagramme est sous-déterminé (le modèle préfère du pseudo-allemand au vrai texte) |

Synthèse d'étape : [`docs/02_synthese.md`](docs/02_synthese.md).

## Dépôt complet et reproductibilité

Ce dépôt rassemble désormais le rapport initial, les transcriptions, les cellules
K01–K19, leurs préinscriptions (K01–K16), résultats et journaux, ainsi que les outils des
analyses K01–K15 et le solveur K16. Les échanges Claude qui documentent le transfert
du travail sont dans [`docs/claude-transcripts/`](docs/claude-transcripts/); les
formes de jetons sont masquées avant publication.

Le détail des résultats K16 se trouve dans
[`experiments/K16_double_lasry/RESULTS.md`](experiments/K16_double_lasry/RESULTS.md).
Le dépôt Actions dédié et ses artefacts restent accessibles dans
[le run de recherche 15–20](https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36733015575).

### Recherche K16 sur GitHub

Dans GitHub, ouvrir **Actions → K16 parallel bottle scan → Run workflow**. Le
workflow effectue une recherche standard sur chaque paire de largeurs 15–20, jusqu'à
20 runners en parallèle. Il conserve le candidat complet et les deux clés dans
chaque artefact, puis classe les scores allemands. Un score élevé reste un indice à
vérifier, pas une résolution sans contrôle du texte et de la puissance.

### Outils et données

- `data/transcription_v1.txt` : transcription retenue de la bouteille.
- `data/transcription_v0.txt` et `data/transcription_corsair_2015.txt` : variantes
  conservées pour comparer les lectures.
- `data/controle_de_kant_6343.txt` : texte de contrôle utilisé dans les analyses.
- `data/ciphertext_979.txt` : flux de 979 lettres préparé pour K16.
- `data/models/qg_de.bin` : modèle de quadrigrammes allemands.
- `data/heldout/de.txt` : texte indépendant du modèle, réservé aux contrôles.
- `tools/` : scripts et sources C de K01–K16 ; `tools/k18/` et `tools/k19/` pour K18–K19 (corpus : `tools/k18/fetch_corpus.sh`).

Les commandes K16 `solve` et `null` prennent le chemin du fichier chiffré en
troisième argument. Le chargeur corrigé lit le contenu du fichier; `solve` affiche
le texte candidat complet. Pour exécuter localement :

```sh
gcc -std=c11 -O3 -march=native -flto -fopenmp -o k16 tools/k16_double_ct2.c -lm
OMP_NUM_THREADS=8 ./k16 solve data/models/qg_de.bin data/ciphertext_979.txt 10 14 3 40000 5 20000 20260930
```

Le mode `K16_IDP_GREEDY=1 K16_K2_POLISH=1` est expérimental et sert au tri rapide;
il ne remplace pas les contrôles de puissance.
