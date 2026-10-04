# B01 — K2 tirée d'une phrase espagnole ou allemande (Wikiquote) — résultats (2026-10-04)

Pré-inscription : `PREREGISTRATION.md`. Sorties : `logs/blume_es/`, `logs/blume_de/` (tranches d'un million de clés).

| Base | Clés | Essais (K2 × w1) | IDP maximale | Candidats ≥ 0,28 |
|---|---:|---:|---:|---:|
| contrôles espagnols plantés (vraie K2 parmi 100 000 leurres) | | | **0,35–0,36** (2/2 en tête) | |
| Wikiquote espagnol (débuts en mots entiers + 11–30 premières lettres) | 3 447 052 | 68 941 040 | 0,185 | **0** |
| Wikiquote allemand (idem) | 1 949 935 | 38 998 700 | 0,181 | **0** |

Toutes les meilleures valeurs sont obtenues à w1 = 30, la largeur la plus grande de la plage (moins de lignes, plus
de liberté d'alignement : le plafond du bruit y est le plus haut), et restent au niveau des meilleurs leurres des
contrôles (≤ 0,18).

## Conclusion (critère pré-inscrit)
**Aucun candidat.** Si le télégramme 1 est une double transposition directe à la convention testée, sa clé K2 n'est le
début (en mots entiers ou coupé à 11–30 lettres) d'aucune des 604 513 phrases de Wikiquote espagnol et allemand. Restent
ouverts : autres sources de phrases (devises, chants, textes politiques de 1936–37, vocabulaire commercial), K2 prise
au milieu d'une phrase, autre convention de dérivation de clé (par exemple numérotation à l'allemande des lettres
répétées), et la recherche conjointe avec le télégramme 2.
