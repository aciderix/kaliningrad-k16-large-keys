# K02 — Contacts entre lettres et réalité des espaces (test de la transposition bloc par bloc) — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul de ces statistiques sur le texte (2026-09-28). Déjà connu sur le texte : fréquences, IC,
longueurs de sections (K01).

## Pourquoi
K01 laisse ouverte l'hypothèse **H-bloc** : chaque section (166, 169, 162, 169, 169, 144 lettres ; 169 = 13², 144 = 12²) est un
morceau d'un texte continu dont les lettres ont été **permutées** (grille, colonnes…), les espaces pouvant être factices. Ce test
n'exige aucune hypothèse sur la langue : toute langue naturelle (même sous une substitution simple) crée une dépendance entre
lettres voisines ; une permutation des lettres la détruit, et une transposition en colonnes d'un carré la déplace à la distance
du côté du carré.

## Données
`data/transcription_v1.txt`, variante A (26 lettres ; apostrophes, accents, soulignements ignorés ; espaces ignorés pour T5).
Paires prises **à l'intérieur d'une même section** (S1..S6 ; « eimat » exclu). Sensibilité : S1..S5.

## Tests
- **T5 — information mutuelle à distance d.** MI(d) = information mutuelle (estimateur direct, en bits) de la table des paires
  (x_i, x_{i+d}), d = 1..40. Null : 2 000 permutations des lettres **à l'intérieur de chaque section** (conserve les comptes de chaque
  section). Rapport : z(d) et p(d) (unilatéral haut).
  - Décision 1 : p(1) < 0,01 ⇒ **contacts présents** ⇒ H-bloc (permutation des lettres dans la section) **rejetée**.
    p(1) > 0,1 ⇒ contacts absents, compatible avec H-bloc.
  - Décision 2 (carré en colonnes non clé) : p(13) < 0,01/40 ou, pour S6 seul, p(12) < 0,01/40 ⇒ signal de grille.
- **T6 — les espaces sont-ils réels ?** Statistique : χ² de la table (lettre × position dans le mot ∈ {initiale, finale, intérieure,
  mot d'une lettre}), variante A, texte entier. Null : 2 000 tirages où la suite des lettres est conservée et les espaces sont
  replacés en permutant au hasard la liste des longueurs de mots. p unilatéral haut.
  Décision : p < 0,01 ⇒ la position dans le mot dépend de la lettre ⇒ **espaces réels** (liés au texte) ; p > 0,1 ⇒ espaces
  compatibles avec des coupures arbitraires.

## Contrôles synthétiques (avant le texte) — texte allemand réservé (Gutenberg 6343), 984 lettres, mêmes tailles de sections
(a) clair ; (b) clair sous substitution simple ; (c) chaque section écrite en lignes dans un carré de côté 13 (12 pour 144 ;
dernière ligne incomplète si besoin) et lue par colonnes dans un ordre de colonnes aléatoire (colonnes à clé) ; (d) idem, colonnes
dans l'ordre (sans clé) ; (e) mots allemands réels sous substitution, espaces réels ; (f) texte (c) recoupé en faux mots avec les
longueurs de mots du cryptogramme.
Attendu : T5 p(1) < 0,01 pour (a) (b) ; p(1) > 0,1 pour (c) (d) ; pic à d = 13 pour (d). T6 p < 0,01 pour (e) ; p > 0,1 pour (f).
Si un contrôle échoue, le test correspondant est déclaré sans puissance.

## Portée
Un rejet de H-bloc laisse ouvertes : substitution (simple, homophone, avec variantes), transposition de **mots** ou de syllabes,
langue inventée ou texte sans langue. Aucune lecture n'est proposée ici.
