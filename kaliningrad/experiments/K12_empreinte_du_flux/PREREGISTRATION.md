# K12 — Empreinte du flux de 979 lettres contre des familles de chiffres synthétiques — PRÉ-INSCRIPTION

Rédigée et commitée avant tout calcul (2026-09-29). Suite de K10-K11 : les espaces sont une couche de présentation ; on analyse le
flux sans espaces (variante A, 26 lettres, 979 lettres, blocs S1-S6 à la suite).

## Question
À quelles familles de procédés le flux ressemble-t-il, sans supposer le système : texte naturel, substitution, Vigenère,
transposition, transposition + substitution, Playfair, Bifid (fractionnement Polybe + transposition), substitution homophonique,
chaîne artificielle (lettres tirées indépendamment) ?
**Limite annoncée d'avance** : une transposition (avec ou sans substitution) et une chaîne artificielle tirée lettre à lettre ont
la même empreinte (fréquences conservées, aucun contact) ; K12 ne peut pas les séparer. Son but est d'exclure formellement les
autres familles et de décrire précisément ce qui reste compatible.

## Statistiques (vecteur d'empreinte)
E1 IC (26 lettres) ; E2 MI(1) − moyenne de MI(1) sur mélanges ; E3 idem MI(2) ; E4 max sur p = 2..20 de l'IC moyen des p
sous-suites (signature polyalphabétique) ; E5 χ² entre distributions des lettres aux positions paires et impaires (signature
digraphique / fractionnement) ; E6 nombre de lettres identiques aux positions (2k, 2k+1) (Playfair : 0) ; E7 nombre de lettres
distinctes ; E8 excès de trigrammes répétés sur mélanges.

## Familles (200 échantillons de 979 lettres chacune, à partir de l'allemand réservé et, pour la robustesse, du néerlandais)
F1 clair ; F2 substitution simple ; F3 Vigenère (clé de 3 à 12) ; F4 transposition en colonnes (clé de 5 à 20) ; F5 substitution
+ transposition ; F6 Playfair (clé aléatoire, j→i, doublets séparés par x) ; F7 Bifid (période 5 à 10) ; F8 homophonique (26
symboles répartis proportionnellement aux fréquences) ; F9 chaîne artificielle i.i.d. aux fréquences allemandes ; F10 chaîne i.i.d.
aux fréquences de la bouteille.

## Décision
Pour chaque famille, la bouteille est dite **compatible** si chacune des 8 statistiques tombe dans l'intervalle central à 99,5 % de
la famille (correction pour 8 statistiques ≈ 4 % de faux rejet global par famille). **Exclue** sinon, en nommant la statistique.
Rapport : tableau famille × statistique (percentile de la bouteille).
Contrôle : chaque famille, jugée sur un échantillon supplémentaire d'elle-même, doit être déclarée compatible avec elle-même
≥ 90 % du temps, et F1-F3, F6-F8 doivent être distinguables entre elles.

## Amendement 1 (avant le texte réel)
Premier passage des contrôles avec 200 échantillons par famille : auto-compatibilité 0,82-0,85 pour F1, F3, F7 (< 0,90 exigé) —
bornes à 99,5 % mal estimées sur 200 tirages. Passage à **1 000 échantillons par famille** ; critères inchangés. Homophonique (F8) :
26 symboles, les 14 lettres les plus fréquentes reçoivent 1 ou 2 symboles, les 12 plus rares partagent un symbole existant (fusion).
