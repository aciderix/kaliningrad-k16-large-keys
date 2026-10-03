# K19 — Chiffres « d'écolier » et mélange local (2026-10-03)

Statut : **exploration** (non pré-inscrite), sauf un test dont la prédiction a été fixée avant le calcul (§ 3.4).
Chaque test est calibré par des mélanges de la bouteille et, quand c'est pertinent, par des contrôles de puissance sur
de l'allemand chiffré. Outils : `tools/k19/` (bibliothèque commune `tools/k18/`, corpus : `tools/k18/fetch_corpus.sh`,
puis `K18_CORPUS=<dossier>`) ; sorties : `logs/`.

**Résultat d'ensemble : aucun déchiffrement**, mais une observation structurelle nouvelle : les lettres semblent
n'avoir été **déplacées que localement** (sur une vingtaine à une quarantaine de positions), et non mélangées sur tout
le texte.

## 1. Sources de presse (2015)

Articles encore en ligne : NEWSru (02/07/2015), copie LiveJournal de l'article de *Strana Kaliningrad*, KP, Vesti,
PGTRK. Ils précisent : **deux** feuilles de cahier roulées, serrées par de la feuille d'aluminium puis du fil de cuivre ;
bouchon de liège de type champagne scellé à la cire ; bouteille brune « tchebourachka » (bière ou limonade soviétique),
brisée et jetée par les ouvriers. Vesti ne publie qu'un recadrage de la même photo 688 × 841. S. Aleshnikov
(université Kant) : « il n'est pas exclu que ce soient des enfants […] ces jeux étaient populaires à l'époque soviétique ».
Conséquence : le texte dont on dispose est très probablement **complet**.

## 2. Chiffres « d'écolier » à clé fixe : aucun

| Famille | Portée | Contrôles (allemand chiffré) | Bouteille |
|---|---|---|---|
| permutation périodique : groupes de p lettres permutés par la même clé (« шифр перестановки » des manuels, carré magique), score bigrammes allemands (`periodic*.py`) | p = 2–64 ; alignement global et par section | clé exacte 3/3 jusqu'à p = 25 avec 10 % de nuls f/w/n, jusqu'à p = 36 sans nuls ; au-delà la recherche s'arrête avant l'optimum | meilleur score 0,12 par paire (p = 64), jamais au niveau d'un clair (+0,2 avec nuls, +0,45 à +0,55 sans) |
| idem, score MI (substitution quelconque, toute langue) | p = 2–25 | 3/3 jusqu'à p = 16 ; partiel à 20–25 | MI 0,22–0,32 = nuls (vraie remise en ordre 0,66–0,78) |
| **grille tournante de Jules Verne** (*Mathias Sandorf*) 4×4, 5×5, 6×6, 7×7 : **toutes** les grilles (256 ; 4 096 ; 262 144 ; 16 777 216), 2 sens de rotation, chiffré lu en lignes ou en colonnes, tous les décalages (et par section pour 4–6), clair inversé (`grille*.py`, `grille7.c`) | recherche exhaustive | 3/3 dans chaque cas pour 4–6 (avec 10 % de nuls et clair inversé) ; 7×7 : clé exacte retrouvée (+0,30 avec nuls) | −0,47 ; −0,42 ; −0,37 ; −0,36 par paire (nuls : max −0,45 ; −0,41 ; −0,39 ; −0,38) : illisible |
| chaque **ligne** du manuscrit chiffrée avec la même clé : colonnes à clé w = 2–8 (toutes les clés), zigzag 2–8 rails, inversion (`perline.py`) | 25 lignes | contrôle w = 6 : clé exacte (+0,52) | −0,46 (nuls −0,43 à −0,48) |

Non couverts : grille 8×8 (4¹⁶ clés), clés changeant d'une ligne à l'autre.

## 3. Observation nouvelle : un reste d'ordre à courte distance

### 3.1 Score bigrammes allemands entre lettres proches (`bigscore.py`, `bandrep.py`)
Moyenne sur les distances 1–10 du score symétrique log P(b|a)/P(b) : **z = +3,1** contre 1 000 mélanges (p < 0,001).
Reproduit sur la transcription indépendante de Corsair (+2,9), sur les lignes impaires (+2,35) et paires (+1,39), sur
chaque page (+2,6 ; +1,8) et sur les seules paires internes aux lignes (+2,7). Ampleur : +0,06 par paire, la moitié de
celle d'un allemand lu dans l'ordre (+0,11).

### 3.2 Échelle (`scale.py`) — z par bande de distances (contrôles : moyenne de 5 textes allemands transformés)

| | 1–2 | 3–5 | 6–10 | 11–20 | 21–40 | 41–80 |
|---|---:|---:|---:|---:|---:|---:|
| **bouteille** | **+1,9** | **+1,2** | **+2,0** | **+0,7** | **+1,5** | **−0,2** |
| anagramme mot par mot | +8,1 | +2,4 | +0,5 | −0,2 | 0,0 | −0,5 |
| tranches de 10 lettres mélangées | +5,0 | +4,6 | +1,3 | +0,7 | −0,1 | −0,1 |
| tranches de 20 | +2,5 | +2,3 | +2,8 | +0,7 | −0,2 | +0,1 |
| tranches de 40 | +0,9 | +1,1 | +1,5 | +2,0 | +0,3 | +0,1 |
| permutation périodique p = 36 | +0,8 | +1,4 | +1,9 | +1,3 | +1,2 | −0,2 |
| déplacements aléatoires ≤ 30 | +0,9 | +1,8 | +2,3 | +2,0 | +0,7 | +0,2 |
| colonnes à clé (13) ; double transposition | ≈ 0 | ≈ 0 | ≈ 0 | ≈ 0 | ≈ 0 | ≈ 0 |

Compatible avec un mélange sur **20 à 40 positions** ; incompatible avec l'anagramme mot par mot (trop fort à distance
1–2) et avec les transpositions globales (≈ 0 partout). Bruit : environ ±1 par bande.

### 3.3 Les lettres liées en allemand restent proches (`cooc.py`, `ctest.py`, `cdist.py`)
- L'enrichissement des paires à distance ≤ 10 dans la bouteille suit celui de l'allemand (r = +0,15, p = 0,02).
- **c** : en allemand, il est presque toujours collé à h ou k (ch, sch, ck). Dans la bouteille, **16 des 17 c ont un
  h ou un k à moins de 10 positions**, contre 11 attendus (p = 0,008), mais seulement 8 à moins de 3 positions :
  les c sont restés près de leur h/k, **déplacés de quelques positions**. Les distances observées (1–9, une à 15)
  sont mieux expliquées par un mélange par tranches de 20–40 que par un mélange global (≈ 2 unités log) ou par
  tranches de 10 (≈ 3 unités log).

### 3.4 Test à prédiction fixée avant calcul : régularité des voyelles (`vowelreg.py`)
Prédiction : si le mélange est local, le nombre de voyelles par fenêtre est plus régulier que dans un mélange global
(z < −2). Bouteille : W = 10 : −0,8 ; W = 20 : **−1,7 (p = 0,035)** ; W = 40 : **−1,6 (p = 0,033)**. Sens prédit,
**seuil non atteint**. Contrôles : allemand dans l'ordre −6,1 / −4,4 / −3,1 ; tranches de 40 −1,9 / −1,8 / −1,8 ;
période 36 −2,1 / −1,8 / −2,3 ; colonnes à clé ≈ 0.

### 3.5 Unités du mélange (`crossline.py`, `segheter.py`, `localnull.py`)
Paires dans une même ligne : z = +2,4 ; paires à cheval sur un retour à la ligne : +0,4 (sections : +2,1 / +0,45).
Écart suggestif mais non décisif (moins de paires à cheval) ; le test direct du § 3.10 montre que les lignes ne sont
pas les unités du brassage. L'hétérogénéité de composition entre lignes n'est pas significative (z −1,6 à +0,1).

### 3.6 Les lignes se laissent mieux réarranger en allemand que des lignes factices (`anagram.c`)
Recuit sur l'ordre des lettres de chaque ligne (multiensemble fixé), noté aux quadrigrammes allemands joints
(`data/models/qg_de.bin`), 10 départs × 400 000 itérations, 3 graines. Score moyen du meilleur arrangement par
quadrigramme :

| Lignes | Score | Lecture |
|---|---:|---|
| **bouteille (25 lignes, 3 graines)** | **−7,63** | |
| factices A : lettres de la bouteille rebrassées sur tout le texte (40 jeux) | −7,84 ± 0,075 (max −7,66) | bouteille au-dessus des 40 jeux, z = +2,8 |
| factices B : idem, mais même nombre de voyelles que chaque vraie ligne (40 jeux) | −7,75 ± 0,036 (max −7,69) | bouteille au-dessus des 40 jeux, z = +3,3 |
| allemand réel, lignes de mêmes longueurs, lettres mélangées | −7,54 | |

L'avantage ne tient donc pas seulement à l'équilibre voyelles/consonnes. Les arrangements obtenus restent du
pseudo-allemand (« wollenderklichtdersteinen… ») et les f en trop restent rejetés en bout de ligne : **aucune
lecture**. Les procédés de mélange par ligne à règle simple (une lettre sur k, k = 2–15 ; alternance début/fin) ne
donnent rien (`perline2.py` : −0,50 contre −0,46 à −0,56 pour les nuls ; contrôle retrouvé à +0,55).

### 3.7 Déplacements limités : le signal est le plus fort pour de petits déplacements
Même recuit, mais chaque lettre ne peut s'éloigner que de D positions de sa place dans la bouteille (option D de
`anagram.c`), 10 jeux factices A :

| D | bouteille | factices | z |
|---:|---:|---:|---:|
| 3 | −9,49 | −9,90 ± 0,08 | **+5,3** |
| 5 | −8,65 | −8,99 ± 0,07 | **+4,8** |
| 10 | −8,15 | −8,31 ± 0,06 | +2,7 |
| 20 | −7,85 | −8,04 ± 0,07 | +2,9 |

Forme comparée à des contrôles (allemand + 10 % de nuls f/w/n, un tirage chacun, `dshape.py`) : tranches de 20
lettres mélangées +5,7 / +5,0 / +3,2 / +3,5 (**la plus proche**) ; tranches de 40 +4,0 / +6,7 / +5,7 / +3,1 ;
tranches de 4–10 et déplacements ≤ 4–16 : écarts deux à trois fois plus forts ; allemand non mélangé +15 / +10 / +6 / +4.

### 3.8 Quelle langue le mélange local a-t-il conservée ? (`langband.py`)
Même signal (§ 3.1) mesuré avec les bigrammes de chaque langue : poésie allemande +3,8, bas-allemand +3,8, allemand de
Pennsylvanie +3,4, allemand +3,4, français +3,5, anglais +2,4, russe translittéré à l'allemande +2,1, polonais +1,8,
néerlandais +1,7 ; finnois, espagnol, italien, latin, russe en translittération savante, portugais : +0,3 à +1,2.
La famille allemande est la mieux placée ; avec le décompte des lettres (w fréquent, ê/ö/ü), l'allemand reste le
candidat le plus probable pour le texte brassé.

### 3.9 Limite de principe : un anagramme par tranches ne se déchiffre pas par les fréquences
Contrôle : allemand + 10 % de nuls, mélangé par tranches de 20 lettres **à découpe connue** ; recuit sur l'ordre
interne des tranches avec raccords entre tranches (`chunkana.c`). Le meilleur arrangement trouvé note **−8,77**, le
vrai texte **−11,02** : le modèle préfère des dizaines de pseudo-allemands au clair. Ce n'est pas un défaut de
recherche ; avec des tranches d'une vingtaine de lettres, la remise en ordre est **sous-déterminée** pour tout modèle
de lettres. Le balayage des découpes (taille, point de départ) retrouve approximativement le point de départ sur le
contrôle (8 au lieu de 7), mais la taille ne se lit qu'à la dispersion des scores entre points de départ.

### 3.10 Où sont les tranches ? (`chunkscan.py`, `linechunk.py`)
- Découpes régulières, tailles 10–44, tous les points de départ : la dispersion des scores entre points de départ reste
  entre 0,030 et 0,073 (maximum à 13, comme pour 10–12) ; sur le contrôle à découpe connue (20, départ 7), la bonne
  taille se signale par 0,12 et le départ est retrouvé à une position près. **Aucune découpe régulière** dans la bouteille.
- Lignes du manuscrit comme tranches : moins bien que 24 découpes de mêmes longueurs décalées (z = −1,2) ;
  demi-lignes : z = +1,4. Le brassage **n'a pas été fait ligne par ligne** : il précède la mise en page, comme les
  espaces (K10).

## 4. Décompte et genres de textes (`genre.py`)
Maximum de f + w sur ≈ 40 000 fenêtres de 979 lettres (prose, Heine, comptines, bas-allemand, allemand de
Pennsylvanie, Bible Schlachter 1951) : 61–63, contre 82. Aucune fenêtre au même décompte (une transposition exacte
d'une source donnerait un écart ≈ 0 ; minimum observé 28,9). Les chants de Prusse-Orientale (*Ostpreußenlied*,
*Zogen einst fünf wilde Schwäne*), riches en f, w, n, sont trop courts pour 979 lettres.

## 5. Conclusion

> **Nuance (K20, même jour)** : le reste d'ordre est établi au niveau des paires de lettres ; au niveau des mots,
> la structure à plusieurs lettres est plus faible que pour un brassage par 20 (repérage de mots Z ≈ +1,2) et la
> présence de vrais mots n'est ni démontrée ni exclue. Voir `experiments/K20_blocs_et_mots/RESULTS.md`.

1. **Non déchiffrée.** Exclus en plus : permutations périodiques à clé fixe (p ≤ 25 avec nuls, ≤ 36 sans), grilles
   de Verne 4×4 à 7×7, transpositions par ligne à clé commune (colonnes, zigzag, une lettre sur k, alternance des
   extrémités, inversion).
2. **Indices convergents d'un mélange local**, mesurés de six façons (score de bigrammes à courte distance z = +3,1 ;
   c près de h/k p = 0,008 ; co-occurrences p = 0,02 ; régularité des voyelles p ≈ 0,03 ; anagrammes par ligne
   z = +2,8 à +3,3 ; déplacements limités z = +5,3), en partie a posteriori mais concordants et reproduits sur la
   transcription indépendante : un texte **de type allemand** dont les lettres ont été brassées à l'intérieur de
   tranches d'une **vingtaine de lettres**, irrégulières et indépendantes des lignes du manuscrit (§ 3.10), **sans clé
   répétée**.
   Cela corrige K18 § 4 : pas de lettres inventées au fil de la plume, mais pas non plus un mélange de tout le
   texte. Les chiffres globaux (double transposition à grandes clés, K16) deviennent peu plausibles.
3. **Limite de principe** (§ 3.9) : un tel anagramme par tranches ne se défait pas par les fréquences de lettres ;
   le modèle trouve toujours un pseudo-allemand mieux noté que le vrai texte. Le message ne pourrait être retrouvé
   qu'avec une information extérieure sur son contenu (noms, date, lieu, texte source connu), ou si l'auteur a suivi
   une règle à clé encore non testée (grille 8×8, clé changeant à chaque ligne).
4. Portrait cohérent avec l'ensemble K01–K19 : un enfant ou un adolescent formé à l'écriture cyrillique écrit un
   texte en allemand (orthographe irrégulière : trop de f, w, n), en brasse les lettres par petits paquets, puis
   déguise le résultat en « texte » (espaces aux rencontres voyelle-voyelle ou consonne-consonne, apostrophes façon
   signe mou, abréviations sur les grappes de consonnes, « i » isolé).
