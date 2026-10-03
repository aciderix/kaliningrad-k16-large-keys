# K21 — Échelle du brassage, lettres nulles, recherche du texte source (2026-10-03)

Statut : **exploration** (non pré-inscrite), calibrée par simulations, mélanges et sources plantées. Outils :
`tools/k21/` (bibliothèques `tools/k18/`, `tools/k19/` ; corpus `K18_CORPUS`) ; sorties : `logs/`.

## 1. Quelle est l'échelle du brassage ? (`abc.py`, `abc2.py`)

Estimation par simulation (ABC) : de l'allemand réel (6 livres), une proportion q de nuls f/w/n (0 à 25 %), puis
chaque lettre déplacée au hasard d'au plus s positions (« jitter ») ou mélange par paquets de s lettres (s = 1 à 120) ;
statistiques résumées : score de bigrammes symétrique sur 6 bandes de distances (1–2, 3–5, 6–10, 11–20, 21–40, 41–80),
centré sur son espérance exacte sous permutation ; 3 000 simulations par modèle ; 3 % les plus proches retenues.

| Modèle | échelle s : médiane (90 %) | nuls q |
|---|---|---|
| déplacements au hasard ≤ s | **53 (26–101)** | non contraint (0,01–0,23) |
| paquets de s lettres mélangés | **57 (25–106)** | non contraint |

Proportion de simulations dans la zone retenue : s ≤ 10 : 0 % ; 11–25 : 1,1 % ; 26–50 : 5,5 % ; 51–80 : 4,3 % ;
81–120 : 2,1 % ; **mélange global : 0/600 ; aucun brassage : 0/300**.

Lecture : les lettres semblent avoir été déplacées sur **une cinquantaine de positions** (de 25 à une centaine),
ni plus (mélange de tout le texte : jamais compatible), ni beaucoup moins. Cela corrige l'estimation « une vingtaine
de lettres » de K19, fondée sur un seul tirage par contrôle.

## 2. Quel geste ? Pas « une lettre sur deux » (`skipgram.py`)

Écrire une lettre sur deux d'un paquet puis les autres rend adjacentes des lettres séparées de 2 dans le clair. Score
des paires de la bouteille avec les statistiques allemandes de lettres séparées de k positions (z contre 1 500
mélanges) : à distance 1, k = 1 (voisines) +1,2 ; k = 2 −0,2 ; k = 3 −1,4 ; k = 4 +1,8. Aucune signature de saut ;
c'est la statistique des **voisines** du clair qui explique le mieux le signal à courte distance (+1,2 à +1,6 aux
distances 1–3), sans sens de lecture (K20 § 4 ; c → h/k : partenaire après 10 fois, avant 7 fois).

## 3. Lettres nulles ? (`nullid.py`)

Pour chaque lettre, corrélation entre son voisinage local (±10) dans la bouteille et celui de l'allemand (z contre
300 mélanges). Bouteille : h +2,7, n +2,1, **f +1,8**, d +1,8, c +1,8, a +1,7 … **w −0,4**, s −0,5, m −1,2, t −1,3.
Contrôle (nuls f et w plantés) : les nuls tombent en bas (f −0,2, w +0,4), mais avec des lettres rares. Le **f** de
la bouteille se comporte comme une lettre du texte, pas comme un bourrage ; le **w** est suspect sans preuve.

## 4. Recherche du texte source par alignement des compositions locales (`srcalign.py`, `srcscan.py`, `shortalign.py`)

Principe : un brassage local conserve, dans l'ordre, la composition de chaque portion du texte. On retire f, w, n
(nuls possibles) de la bouteille et du texte candidat, on découpe la bouteille en 19 fenêtres de 40 lettres et on
cherche la position du candidat où la suite des compositions coïncide le mieux (distance du χ² cumulée).

Puissance (source plantée dans un roman de 600 000 lettres) : brassage par 20 avec 10 % de nuls → position exacte,
score **21,7** (meilleur concurrent 148) ; brassage par 60 avec 15 % de nuls → **65,5** (concurrent 146). Textes
courts (`shortalign.py`, fenêtres de 30) : source de 400 lettres plantée → **2,2** contre 7,0 au mieux pour des textes
sans rapport.

Textes examinés (résultats complets en § 4 bis) :
- 21 romans et essais du corpus K18, poésie (Heine, comptines, bas-allemand, allemand de Pennsylvanie) : meilleur 153 ;
- Bibles : Luther 1912 (156,3), Schlachter 1951 (156,4), Bible synodale russe translittérée (254) ;
- 436 livres allemands de Gutenberg classés poésie, chants, contes, enfance, lectures : meilleur 142,8 (niveau du
  hasard pour un tel volume ; une vraie source donnerait 20–65).

## 5. Grilles tournantes plus grandes (8×8 à 13×13), une seule clé (`grille_sa.c`)

L'échelle du § 1 (≈ 25–100 positions) correspond à des blocs de 49 à 169 lettres. La 7×7 est exclue (K19,
exhaustive). Pour n = 8 à 13, recuit sur les choix de trous (une case par orbite), pour chaque décalage, sens du clair,
sens de rotation et lecture du chiffré ; score bigrammes allemands par paire. Vérifié sur 6×6 (même optimum que la
recherche exhaustive).

| n | contrôle planté (allemand + 10 % de nuls) | bouteille | flux mélangés |
|---|---|---:|---:|
| 8 | grille et décalage exacts, +0,23, clair lisible | −0,356 | −0,365 ; −0,366 |
| 9 | exacts, +0,21 | −0,297 | −0,315 ; −0,324 |
| 10 | exacts, +0,26 | −0,272 | −0,298 ; −0,304 |
| 11 | exacts, +0,15 | −0,225 | −0,240 |
| 12 | décalage exact, clair lisible (+0,29) | −0,198 | −0,231 |
| 13 | exacts, +0,29 | −0,120 | −0,178 |

Grilles 8×8 à 13×13 à clé unique **exclues** : la bouteille reste juste au-dessus des flux mélangés (reste d'ordre
local ; l'écart grandit avec n, car moins de blocs laissent plus de prise au recuit), très loin du niveau d'un clair.
Avec K19 (4×4 à 7×7 exhaustives) et K05 (12×12, 13×13 par section), toutes les grilles tournantes à clé unique de
4×4 à 13×13 sont écartées.

## 4 bis. Recherche élargie : tout l'allemand de Gutenberg, 11 192 chants

| Corpus | Taille | Meilleur alignement | Lecture |
|---|---|---:|---|
| **tous les livres allemands de Project Gutenberg** (catalogue 2026 : 2 404 textes, 2 386 téléchargés) | ≈ 1 milliard de lettres | 142,8 (lot prioritaire) ; 146,2 et 146,9 (autres lots) | niveau du hasard ; une source donnerait 20–65 |
| **volksliederarchiv.de** : 11 192 chants (API WordPress, 113 requêtes), mis bout à bout | 9,1 millions de lettres | 154,1 | niveau du hasard |
| les mêmes chants, chacun aligné sur une portion de la bouteille (`shortalign.py`, fenêtres de 30) | 10 448 chants assez longs | 5,70 (chant de 6 fenêtres) | niveau du hasard : sources plantées 1,1–2,3 ; 2 000 extraits allemands sans rapport : minimum 5,35–7,47 selon la longueur (`shortcal.py`) |
| Bibles : Luther 1912 (eBible.org), Schlachter 1951, synodale russe translittérée | | 156,3 ; 156,4 ; 254 | |

**Aucun texte source trouvé.** Si la bouteille est un texte connu brassé localement, ce n'est ni un livre allemand de
Gutenberg, ni un chant de volksliederarchiv.de, ni une de ces Bibles. Restent possibles : un texte absent de ces
corpus (manuel scolaire soviétique, presse, lettre), ou une composition personnelle — auquel cas aucune recherche de
corpus ne peut aboutir.

## 6. Les « bribes de texte clair » des réarrangements sont des artefacts (`fragments.py`)

Les réarrangements de K19 (lettres déplacées de 3 ou 5 positions au plus, modèle de quadrigrammes allemands) font
apparaître des suites d'allure allemande (« deine … welchen lasse … einem », « er und er sehen diesen … wenn »). Même
traitement sur 10 jeux de lignes factices (lettres de la bouteille rebrassées sur tout le texte) :

| Déplacement maximal | part des lettres prises dans des mots allemands (≥ 4 lettres) : bouteille | lignes factices |
|---|---:|---:|
| 3 | 0,348 | 0,368 ± 0,026 |
| 5 | 0,450 | 0,474 ± 0,031 |

Les lignes factices donnent **autant de mots, et des bribes aussi convaincantes** (« … weist … hofe … leuten »,
« wort … deines ist und er lied… »). Ces fragments sont fabriqués par le modèle de langue à partir de n'importe quel
mélange de lettres ; ils ne sont **pas** du texte clair retrouvé. Le score de quadrigrammes plus élevé de la bouteille
(K19 § 3.7, z = +5,3) traduit le reste d'ordre local entre paires de lettres, pas des mots lisibles.

## 7. Conclusion

1. **Échelle** : les lettres ont été déplacées sur ≈ 25–100 positions (médiane ≈ 55) ; ni mélange de tout le texte,
   ni petits déplacements ; un brassage par section (≈ 166) est environ 5 fois moins compatible.
2. **Geste** : pas « une lettre sur deux », pas de sens de lecture, aucune grille tournante à clé unique de 4×4 à
   13×13, aucune permutation périodique à clé fixe (K19).
3. **Nuls** : le f se comporte comme une lettre du texte ; le w est suspect ; rien de démontré.
4. **Source** : ni Gutenberg allemand (2 386 livres), ni 11 192 chants populaires, ni les Bibles de Luther,
   Schlachter et synodale. La méthode retrouverait pourtant une source même brassée par 60 avec 15 % de nuls.
5. **Bribes de texte** : artefacts, aussi nombreux sur des lignes factices.
6. Le message, s'il existe, est un texte de type allemand absent de ces corpus (composition personnelle, manuel,
   lettre), brassé localement à la main : il n'est pas récupérable par des méthodes statistiques.
