# K27 — Double transposition à clés-mots : résultats (2026-10-03)

Pré-inscription : `PREREGISTRATION.md` (commitée avant de voir le résultat). Outils : `tools/k27/` ; sorties : `logs/`.

## Ce qui a été cherché

Toutes les paires de clés d'un dictionnaire, pour une double transposition en colonnes (incomplète) — la seule
famille classique « à clé longue » que K08, K14 et K16 n'avaient pas pu couvrir avec une puissance suffisante :

| Liste de clés | Contenu | Clés distinctes |
|---|---|---:|
| principale (`keys.py … 20000 20000`) | 20 000 mots allemands et 20 000 mots russes les plus fréquents (FrequencyWords) ; russe numéroté dans l'ordre **cyrillique** et, translittéré, dans l'ordre latin ; ä→a / ä→ae, ß→ss ; ≈ 100 mots thématiques (Heimat, eimat, Pillau, Baltijsk, Königsberg, Ostsee, родина, Балтийск, флот, тайна, шифр…) | 28 380 |
| complémentaire (`keys_extra.py`) | prénoms russes (et diminutifs) et allemands, noms de lieux, expressions de deux mots thématiques (« meineheimat », « konigsbergbaltijsk », « наширодина »…) | 5 666 |

Longueurs 4 à 24. Même clé deux fois (Übchi) comprise. Variantes : à chaque étape, ordre de la clé à l'endroit ou à
l'envers, et étape dans le sens direct ou inverse (16 combinaisons). Texte entier, et chaque bloc chiffré séparément
avec la même paire. Note : quadrigrammes allemands ; criblage sur 120 lettres (seuil −12,8), puis texte entier.

## Contrôles (`tools/k27/controles.sh`, `logs/controles.out`)

Allemand réservé (Kafka) + 99 nuls f/w/n, chiffré avec deux clés tirées du dictionnaire : **10/10 retrouvés en
tête** (texte entier et par bloc, variantes de base et 16 variantes), note complète −10,8 à −11,4 ; les paires
fausses ne dépassent jamais −12,8 au criblage.

## Bouteille

| Recherche | Paires × variantes notées | Meilleur criblage | Meilleure note complète | Lecture |
|---|---:|---:|---:|---|
| liste principale, texte entier, 4 variantes | 3,22 × 10⁹ | −12,0 | **−14,64** | illisible |
| liste principale, par bloc, 4 variantes | 3,22 × 10⁹ | −13,3 | (aucune paire au seuil) | — |
| complémentaire × principale (dans les deux ordres), texte entier, 4 variantes | 1,29 × 10⁹ | −11,8 | **−14,82** | illisible |
| complémentaire × principale (dans les deux ordres), par bloc, 4 variantes | 1,29 × 10⁹ | −13,1 | (aucune paire au seuil) | — |
| liste principale, 12 variantes « sens inverse », texte entier | 9,67 × 10⁹ | −11,8 | **−14,82** | illisible |
| liste principale, 12 variantes « sens inverse », par bloc | 9,67 × 10⁹ | −13,0 | (aucune paire au seuil) | — |
| complémentaire × principale (dans les deux ordres), 12 variantes « sens inverse », texte entier | 3,86 × 10⁹ | −11,8 | **−14,82** | illisible |
| **total** | **3,22 × 10¹⁰** | | **≤ −14,6** | |

Non couvert : liste complémentaire × 12 variantes « sens inverse » par bloc (la liste principale l'est).

Le criblage sur 120 lettres atteint au mieux −11,8 à −12,0 pour une poignée de paires sur des milliards (fluctuation
attendue sur un si grand nombre d'essais) ; sur le texte entier, ces mêmes paires retombent à −14,6 ou moins.

Pour comparaison (même note) : un clair allemand avec 10 % de nuls ≈ −11 ; la bouteille telle quelle −15,47 ; ses lettres
mélangées −15,6 en moyenne (K28). Les meilleures notes ci-dessus sont les maxima de milliards d'essais sur des
lettres sans ordre.

## Conclusion (critère pré-inscrit)

Aucune paire n'atteint −12,0 sur le texte entier (meilleure note −14,64, au niveau des maxima obtenus sur des lettres
sans ordre) ; les contrôles plantés sont retrouvés 10/10 avec 10 % de nuls. Selon le critère fixé avant le calcul,
**la double transposition en colonnes dont les deux clés sont des mots de ces listes est exclue** — texte entier et
par bloc, Übchi compris, mots allemands, russes (ordre cyrillique ou latin), prénoms, lieux, expressions de deux mots,
16 variantes de lecture. Restent non couvertes les clés hors dictionnaire (mots rares, phrases longues, suites de
nombres) et les clés quelconques (K16, sans puissance au-delà de 14 colonnes).
