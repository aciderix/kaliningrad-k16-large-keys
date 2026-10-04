# Synthèse d'étape (2026-09-29) — ce que le cryptogramme n'est pas, ce qu'il peut encore être

Niveaux : CONNU (sources / transcription), RÉSULTAT (test pré-inscrit, contrôles réussis), OBSERVATION (exploration, sans valeur
de preuve), HYPOTHÈSE.

## 1. Faits établis
- CONNU : transcription v1, confirmée par une transcription indépendante (Corsair_nv, 2015) et par les longueurs de blocs de
  Norbert (2017) : 6 blocs de **166, 169, 162, 169, 169, 144** lettres terminés chacun par **une lettre soulignée suivie d'un
  point**, puis « eimat » et une rangée de points.
- RÉSULTAT (K02) : **aucun lien entre lettres voisines** (z = 0,5 ; une langue, même chiffrée par substitution, donne z ≈ 37-40).
- RÉSULTAT (K04) : **pas de mots répétés** (182 formes distinctes sur 194 mots ; jamais observé en prose dans 13 langues).
- RÉSULTAT (K02-T6) + OBSERVATION : les espaces ne sont pas posés au hasard (« i » isolé 7 fois ; n et t en fin de mot ; les 9
  abréviations ne contiennent **aucune voyelle** sur 27 lettres).
- OBSERVATION : les **116 apostrophes suivent toutes une consonne** (n 41, t 28, r 13, d 12, f 6, s 6, l 5, m 3, z 2) : ce ne sont
  pas des signes mélangés avec les lettres ; elles sont attachées à leur lettre.
- OBSERVATION : fréquences les plus proches de l'**allemand** (seule langue compatible parmi 13 pour le profil trié ; e 17,2 %
  comme en allemand), mais **46 f et 36 w** : aucune fenêtre de 979 lettres de 5 textes allemands n'atteint les deux à la fois
  (maximum 41 f). ö (7) et ü (2) présents, ê (17).

## 1 bis. Le schéma qui se dessine (K10, 2026-09-29 ; exploration contrôlée)
- **Établi** : les frontières de mots dépendent anormalement de la paire de lettres qu'elles séparent (on coupe entre deux consonnes,
  deux voyelles ou deux lettres identiques ; z = −6, transcription indépendante −6,5 ; textes réels : jamais sous −2,8).
- **Interprétation (non démontrée)** : texte fabriqué en deux couches, un flux de lettres dans lequel aucun test n'a détecté de
  dépendance, puis un habillage en « mots » (espaces selon les lettres voisines, abréviations en grappes de consonnes, apostrophes
  après consonnes, « i » isolé). Compatible avec un chiffré maquillé comme avec un texte artificiel découpé après coup.
- **K11 (pré-inscrit, confirmé)** : la règle est locale à deux lettres — on coupe quand deux voyelles ou deux consonnes se
  rencontrent, d'autant plus que le mot en cours est long ; l'identité des lettres n'apporte rien (dans une vraie langue, elle est
  le premier prédicteur des espaces). Les « mots » n'ont ni terminaisons ni débuts de langue.
- **K12 (pré-inscrit)** : le flux n'est compatible qu'avec une transposition (± substitution) ou une chaîne tirée lettre à lettre ;
  dans les implémentations testées, clair, substitution, Vigenère, Playfair, Bifid, homophonique sont exclus. Un seul texte découpé
  ou six segments séparés : non décidable par la composition des blocs (puissance 2 %).
- Réserve : la feuille 2 (pâle) ne montre pas l'effet.

## 2. Hypothèses exclues (RÉSULTATS)
| Hypothèse | Test |
|---|---|
| Une langue naturelle lue dans l'ordre, en clair ou sous substitution simple (russe translittéré, ukrainien, finnois, allemand…) | K02 |
| Les mots du clair conservés (substitution fixe, avec ou sans lettres brouillées dans chaque mot) | K04 (+ K01-T4 pour l'allemand) |
| Le même passage chiffré 7 fois (transposition) ; ou sous 7 substitutions | K01 |
| Grille carrée à colonnes (avec ou sans clé) sur les blocs carrés, allemand | K02, K03 |
| Routes classiques (colonnes, zigzags, diagonales, spirales), toutes largeurs, par bloc et texte entier, allemand | K06 |
| Grille tournante (Fleissner) sur les blocs carrés, allemand | K05 |
| Routes ou colonnes à clé (5-40) sur le texte entier **avec substitution en plus, toute langue** (score invariant) | K07 |
| Double transposition en colonnes (clés 3-9), avec ou sans substitution, toute langue | K08 |
| Barrière (rail fence, 2-100 rails) et décimation, blocs et texte entier, avec ou sans substitution | K09 |
| Transposition nihiliste (blocs carrés), Myszkowski (5-15), AMSCO (3-12), ± substitution | K13 |
| Double transposition « même clé » (Übchi) 10-15 colonnes, lettres intactes | K14 |
| Chiffrement par blocs à clé commune : routes (± subst.), colonnes 5-20, Übchi 5-15 (± subst.), grille tournante (± subst.) | K15 |
| Les 6 blocs comme colonnes d'une transposition (liens entre blocs au même rang, décalage ±30) | exploration, p = 0,30 |

## 3. Ce qui reste (HYPOTHÈSES)

> **K17 (2026-09-30)** : le décompte des lettres n'est celui d'aucune fenêtre allemande (f + w = 82 contre 59 au plus),
> et les lettres ne sont pas substituées (lettres absentes = j q x y). Toute transposition, quelle que soit la clé,
> conserve ce décompte : A′ et C sont donc exclues pour de l'allemand ordinaire, sans recherche de clé.
> Voir `experiments/K17_profil_invariant/RESULTS.md`.

> **K18 (2026-10-03)** : liens entre voisines absents même avec les 34 symboles (n', t', ê… distincts) ⇒ toute
> lecture dans l'ordre exclue ; profil trié incompatible avec 11 langues (Bible synodale russe comprise, p ≤ 0,011) ;
> **aucune signature de lettres inventées à la main** (cyclage, suites alphabétiques, évitement des répétitions) ⇒
> le flux est un mélange mécanique d'un stock de lettres. Seul « allemand + ≈ 100 nuls f, w, n » reste à la limite
> (p ≈ 0,07). Les deux « solutions » de Cipherbrain (T. Ernst 2017, « Frank » 2021) n'ont jamais été publiées.
> Voir `experiments/K18_contre_expertise/RESULTS.md`.

> **K19 (2026-10-03)** : les chiffres « d'écolier » à clé fixe sont exclus (permutation de groupes de p lettres,
> grilles de Verne 4×4–7×7 en recherche exhaustive, transpositions par ligne). Mais le flux garde **un reste d'ordre
> à courte distance** (six mesures concordantes, dont c près de h/k et une remise en ordre à déplacements ≤ 3,
> z = +5,3) : un texte de type allemand brassé par tranches d'une vingtaine de lettres, sans clé répétée, puis
> habillé. Un tel brassage ne se défait pas par les fréquences (le modèle préfère du pseudo-allemand au vrai texte).
> Voir `experiments/K19_melange_local/RESULTS.md`.

> **K20 (2026-10-03)** : on travaille sur le **texte entier** (les sections ne sont pas des unités du brassage).
> Le reste d'ordre est sans sens de lecture et de type germanique au niveau des paires de lettres, mais la présence de
> **vrais mots** n'est ni démontrée ni exclue (le test de mots réagit autant à du pseudo-allemand). Voir `experiments/K20_blocs_et_mots/RESULTS.md`.

> **K21 (2026-10-03)** : brassage local sur ≈ 25–100 positions (simulation) ; grilles tournantes à clé unique jusqu'à
> 13×13 exclues ; aucun texte source parmi tout l'allemand de Gutenberg, 11 192 chants populaires et trois Bibles ;
> les « bribes de clair » produites par les réarrangements sont des artefacts (autant sur des lignes factices).
> Voir `experiments/K21_source_et_echelle/RESULTS.md`.

> **K22 (2026-10-03)** : sans information extérieure, le message n'est pas reconstituable : à l'échelle de brassage
> mesurée, la composition locale porte ≈ 0,9 bit par lettre au mieux, moins que l'incertitude d'un texte allemand
> cohérent ; un décodeur mot à mot ne retrouve un contrôle que pour des déplacements de 2 à 4 positions.
> Voir `experiments/K22_reconstruction/RESULTS.md`.

> **K23 (2026-10-03)** : le reste d'ordre local se trouve entièrement **à l'intérieur des « mots »** de l'habillage
> et pas entre eux, contrairement à un allemand brassé puis découpé : il vient probablement de la fabrication des mots,
> pas d'un message. Voir `experiments/K23_signal_dans_les_mots/RESULTS.md`.

> **K24–K25 (2026-10-03)** : aucune grille à trous fixe commune aux blocs ne cache d'allemand (K24). Comparé à
> 97 langues (K25), le décompte reste plus proche de l'allemand que de toute autre langue sans être compatible ; avec
> une substitution en plus de la transposition, 16 langues sur 97 passent le test du profil trié, qui ne peut donc pas
> identifier la langue (nuance de K18). Voir `experiments/K24_grille_fixe/` et `experiments/K25_cent_langues/`.

> **K26–K28 (2026-10-03)** : les lignes délavées sous la page 2 ne sont que la page 1 vue par transparence (K26 :
> pas de texte caché). Une double transposition dont les deux clés sont des mots — ≈ 34 000 clés allemandes et russes
> (ordre cyrillique ou latin), prénoms, lieux, expressions, toutes longueurs, 16 variantes de lecture, texte entier et par
> bloc — est exclue avec des contrôles 10/10 (K27, pré-inscrit). « eimat » / « Heimat » n'est la clé d'aucun procédé
> classique ; la page lue en colonnes et le retrait des lettres marquées (apostrophes, accents, abréviations) ne
> rendent aucun lien entre voisines (K28). Bilan d'ensemble : `docs/03_bilan.md`.

> **K29 (2026-10-03)** : examen de suggestions externes. Nombres en toutes lettres, « sch » écrit w, ê = ä ou э,
> w séparateur de mots : aucun ne rend le décompte allemand. Toutes les marches affines des carrés 13×13 et 12×12
> (dont La Loubère) sont exclues, nuls compris. Les apostrophes ne suivent pas la distribution du signe mou russe ;
> les mots « russes » (gon'it') sont au niveau du hasard. Reste non testable : une grille tournante différente par
> bloc avec ≈ 10 % de nuls. Voir `experiments/K29_suggestions/RESULTS.md`.

> **K30 (2026-10-04, pré-inscrit)** : avec un modèle 6-grammes tolérant aux nuls, une grille tournante différente
> par bloc avec 10 % de nuls est retrouvée 19 fois sur 24 (contre 4/24 aux quadrigrammes) ; les quatre blocs carrés
> de la bouteille restent au niveau de leurs lettres mélangées : **exclue**. Il ne reste plus de famille de
> transposition classique identifiée comme non testable, hormis les clés quelconques très longues (K16) et les
> grilles sur blocs non carrés. Voir `experiments/K30_modele_fort/RESULTS.md`.

- **A′ — allemand (d'un style particulier) mélangé par une transposition à clé plus complexe** (double transposition, grille à
  trous non standard…), espaces et apostrophes ajoutés pour « faire langue ». Pour : absence de contacts et de répétitions,
  profil allemand, ö/ü, blocs réguliers. Contre : excès de f et w jamais vu en allemand ordinaire.
- **C — transposition + substitution** (le profil trié allemand est compatible, p = 0,12) : exclue pour les routes et les colonnes
  à clé sur le texte entier (K07) ; restent les transpositions plus complexes.
- **B — pseudo-texte sans message** (lettres choisies à la main avec des fréquences « allemandes », habillées en mots, blocs
  réguliers). Pour : aucun mécanisme simple ne répond ; les abréviations sans voyelle et le « i » isolé sont des choix d'habillage.
  Contre : une main qui invente produit en général des enchaînements (lettres prononçables, motifs favoris) ; ici, aucun
  enchaînement mesurable (motifs répétés : OBSERVATION marginale, p ≈ 0,03 non retenue).
- Le mot final « eimat » (« Heimat » ?) après le dernier bloc n'est pas expliqué : en clair, il signerait un auteur germanophone.

## 4. Autres observations (explorations)
- Doublets : à l'intérieur des mots, 43 contre 66 attendus (p = 0,0008) ; dans le texte continu, 67 contre 80 (p = 0,06) : les
  lettres doublées tombent volontiers à cheval sur un espace — geste d'habillage (l'auteur coupe entre deux lettres identiques).
- Aucune photo meilleure que les deux images 688 × 841 de 2015 (recherche du 2026-09-29, `00_choix.md`). La presse de 2015
  appelle la bouteille une « tchebourachka » (surnom soviétique d'une bouteille de limonade, lié au dessin animé de 1969) : si
  c'est exact, le dépôt est postérieur aux années 1960 (datation à vérifier, non établie ici).


## 5. Frontière de ce qui est testable ici
Double transposition à deux clés différentes de 10 colonnes et plus, ou à clé répétée de 16 colonnes et plus : nos solveurs
(recuit conjoint, diviser pour régner) n'ont pas la puissance voulue sur des messages plantés (K08, K14). Ni confirmée ni exclue.
