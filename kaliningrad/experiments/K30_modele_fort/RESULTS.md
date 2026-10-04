# K30 — Grille tournante indépendante par bloc, avec nuls, notée par un modèle 6-grammes : résultats (2026-10-04)

Pré-inscription : `PREREGISTRATION.md` (commitée après les contrôles, avant le calcul sur la bouteille). Outils :
`tools/k30/build_lm6.c` (modèle), `tools/k30/fleiss_lm.c` (recherche) ; sorties : `logs/`.

## Pourquoi
Après K29, la seule famille cryptographique déclarée **non testable** était la grille tournante (Fleissner) avec une
clé différente pour chaque bloc carré et ≈ 10 % de nuls : avec les quadrigrammes, la clé n'est retrouvée que 1 à
3 fois sur 12, et de faux arrangements notent mieux que le vrai clair. Le verrou était la fonction de score, pas la
recherche.

## Le modèle
6-grammes de lettres (contexte de 5), lissage de Witten-Bell jusqu'à l'unigramme, mélangé à 10 % avec une loi
uniforme pour absorber les nuls ; appris sur 8,9 millions de lettres (20 livres allemands de Gutenberg, Kafka exclu).
Table dense de 26⁶ octets (309 Mo). Sur un texte réservé : allemand −1,51 nat/lettre, allemand + 10 % de nuls −2,26,
lettres mélangées −4,10.

## Contrôles (Kafka + 10 % de nuls f/w/n insérés, grille et variante au hasard par bloc)

| Score | 13×13 | 12×12 |
|---|---:|---:|
| quadrigrammes (outil de K05, mêmes nuls insérés) | 1/12 | 3/12 |
| **6-grammes tolérant aux nuls** | **10/12** | **9/12** |

Les 5 échecs sont partiels (54 à 153 voisinages retrouvés sur 143–168) ; notes trouvées −2,05 à −2,80 par lettre,
22/24 au-dessus de −2,6.

## Bouteille (même recherche ; 20 mélanges des lettres de chaque bloc)

| Bloc | note réelle | mélanges : moyenne / max | au-dessus des 20 mélanges ? | ≥ −2,6 ? |
|---|---:|---:|---|---|
| S2 (13×13) | −2,915 | −2,924 / −2,874 | non | non |
| S4 (13×13) | −2,919 | −2,891 / −2,826 | non | non |
| S5 (13×13) | −2,840 | −2,839 / −2,761 | non | non |
| S6 (12×12) | −2,870 | −2,841 / −2,779 | non | non |

Les « meilleurs » arrangements (« sfncensruhternfnostwtuewachsen… ») sont du pseudo-allemand, comme sur les mélanges.

## Conclusion (règle pré-inscrite)
Aucun bloc ne remplit les conditions : **l'hypothèse « grille tournante indépendante par bloc, avec ≈ 10 % de nuls »
est exclue pour les quatre blocs carrés.** Avec une puissance de ≈ 0,8 par bloc, la probabilité de manquer les
quatre blocs s'ils étaient tous chiffrés ainsi est de l'ordre de 0,2⁴ ≈ 0,002 ; même un seul bloc chiffré ainsi serait
détecté 4 fois sur 5. Restent hors du test les blocs non carrés S1 (166) et S3 (162).

## Branche « pseudo-texte mécanique » : la composition d'un stock de lettres
Pour tester l'idée d'un tirage dans une « касса букв » ou un jeu de lettres, il faudrait une table de composition
**documentée indépendamment** : sans elle, n'importe quel décompte s'ajuste à un stock imaginé exprès (un paramètre
libre par lettre). Recherche du 2026-10-04 (web, russe et allemand) : les caisses scolaires russes actuelles
comptent ≈ 48 cartes avec deux exemplaires des lettres les plus courantes ; aucune table pour un alphabet latin ou
allemand de l'époque soviétique n'a été trouvée. Les *Gießzettel* d'imprimerie allemands suivent les fréquences de
l'allemand et ne donneraient pas l'excès de f et de w. Cette branche reste compatible avec toutes les mesures mais
n'est pas démontrable sans l'objet ou une telle table.
