# B00 — Vérifications rapides et analyse du paysage (4 octobre 2026)

Outil : `tools/bdt.c` (modes `lag`, `lagcal`, `single`, `probe`, `probefit`, `knownprobe`, `sameprobe`, `ctrl`,
`samectrl`, `samescan`, `dict`). Modèle : `data/models/qg_es.bin` (bigrammes PMI). Clair de contrôle :
`data/heldout/tg_es_58221.txt` (espagnol « télégraphique » tiré de pg58221 par `tools/telegraphese.py` : mots outils
retirés, nombres et mots de commerce insérés, X pour point).

## 1. Le balayage des écarts ne dit rien sur la double transposition directe (correction de l'existant)
Les notes de Bourdeau tirent de son balayage des écarts (z max 3,3 sur T1) un « indice faible » contre une double
transposition directe, parce que ses contrôles directs donnaient z = 5,5–9,1. Ces contrôles prennent tous le même
clair, `txt[7000:7615]` du Quichotte, c'est-à-dire la table des matières (« Capítulo… Que trata de… »), un texte
répétitif qui crée des pics d'écart quel que soit le chiffrement : son propre script le montre, la convention mixte y
pique aussi à des écarts « inattendus » (24, 28, 51…). Sur des clairs tirés au hasard (notre statistique, PMI) :
- double transposition directe, w1 et w2 de 11 à 37 (12 plantés par paire) : z max médian **3,0** partout ;
- T1 : z max **2,8**, au 25e centile de ces plantés.
Le télégramme est donc parfaitement compatible avec une double transposition directe, et le balayage ne renseigne pas
sur les largeurs. Le même calcul montre qu'il n'exclut pas non plus la colonne simple **directe** (chaque écart ne
reçoit qu'une paire de colonnes, ≈ 30 bigrammes sur 600) ; d'où le test suivant.

## 2. Colonne simple (toutes largeurs 2–60) : exclue
IDP de colonne simple (alignement des colonnes de C, plages exactes de fin de colonne), z contre 200 mélanges :
contrôle planté w = 33 → **z = 10,7** à la bonne largeur ; T1 : z max **2,2** (w = 19) ; T2 : z max 1,5.

## 3. Transposition périodique par blocs (Nihilist lue par lignes) : exclue
Blocs de w lettres permutés par la même clé ; colonnes = positions mod w, appariées rangée à rangée : contrôle planté
w = 23 → **z = 15,4** ; T1 : z max **2,3** (w = 2–60) ; T2 : z max 0,7 (w = 2–30).

## 4. Aucun motif positionnel entre T1 et T2
Coïncidences de lettres aux mêmes positions depuis le début (10) et depuis la fin (16) contre 11,1 attendues ; meilleur
décalage quelconque 24 coïncidences, sous le 95e centile (24) du maximum sur des T2 mélangés. Le Z commun en position
13 et les « REF » des derniers groupes (REFLX, REFUD) sont du hasard.

## 5. Pourquoi le recuit sur K2 échoue au-delà de w2 ≈ 15 (mesuré)
Sonde autour de la vraie K2 (échanges de colonnes de même longueur, qui ne déplacent aucune borne) :

| mesure (w1 = 18, w2 = 20) | vraie | 1 éch. | 2 | 3 | 4 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| IDP (K1 inconnue), z | 22,7 | 14,5 | 8,2 | 5,2 | 2,8 | 1,3 | 0,5 |
| « oracle » (K1 vraie connue), z | 19,1 | 15,3 | 12,3 | 10,2 | 8,4 | 5,5 | 4,0 |
| part des colonnes justes | 100 % | 90 % | 81 % | 74 % | 66 % | 55 % | 46 % |

Avec K1 connue, la note décroît comme le carré de la part de colonnes justes (paysage lisse) ; l'IDP, qui doit
re-choisir K1 (meilleur partenaire de chaque colonne parmi ≈ 20 × 10 alignements), s'effondre dès 3–4 échanges :
chaque vraie paire de colonnes de K1 (≈ 30 bigrammes) dépasse à peine le maximum du bruit. Ni une matrice commune
T1+T2, ni des triplets (trigrammes), ni des chaînes de 4 colonnes (quadrigrammes) ne changent la pente (ils relèvent
seulement le z de la vraie clé : 22,7 → 26,3 / 25,4 / 28,8). Le défi Schmeh 2007 (599 lettres, 21 × 23, anglais) a la
même pente (z 16,9 → 2,3 après 3 échanges) ; notre recuit y échoue (0/4, IDP 0,14 contre 0,37), comme celui de Bourdeau.
Lasry l'a cassé par escalade **et** par dictionnaire ; sa méthode d'escalade (article de 2014, thèse de 2018) n'est pas
accessible d'ici (anti-robot, archive web interdite).

Taux de succès par recuit (300 k–1 M itérations, plantés) : 15 × 14 : 23/24 ; 12 × 11 : 8/8 ; 25 × 11 : 6/8 ;
20 × 11 : 11/32 ; 16 × 17 : 0/12 ; 19 × 17 : 0/12. Clé unique (K1 = K2, note quadrigrammes) : w = 15 : 1/4 ;
18 : 8/30 ; 19 : 1/50 ; 20 : 0/50 ; 21 : 0/30.

## 6. Petites listes de clés : rien
- 730 clés thématiques (`data/keys_thematiques.txt` : Oswald, HOVAG, Emser Werke, Salamanca, devises franquistes,
  falangistes, carlistes, chants allemands et suisses, Bührle-Oerlikon…) : aucun z > 4,5.
- 64 053 dates en toutes lettres (1936–1937, allemand, espagnol, français, anglais) : z max 5,4 (bruit).
- Clé unique, w = 11–16, 8 recuits de 200 k : z max 6,5 (une vraie clé donne ≈ 25).
