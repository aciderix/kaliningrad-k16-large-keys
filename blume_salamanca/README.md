# « BLUME SALAMANCA » — deux télégrammes Zurich → Salamanque (8 janvier 1937)

> **Correction (2026-10-04).** Une première version de ce fichier déclarait la cible « sans source, peut-être
> inventée ». C'était faux : la source est le travail de D. Bourdeau, signalé par l'utilisateur
> (https://github.com/dbourdeau/cyphersolver/tree/main/targets/blume), que notre recherche web n'avait pas trouvé.

## Les faits (d'après `targets/blume/NOTES.md` de D. Bourdeau)
- Deux télégrammes envoyés de Zurich le 8 janvier 1937 par le Dr ing. W. E. Oswald (fondateur des Emser Werke),
  adressés « BLUME SALAMANCA » (Salamanque : quartier général de Franco). Trouvés par l'historienne Regula Bochsler
  dans les dossiers de la police fédérale suisse (*Nylon und Napalm*, 2022), publiés par K. Schmeh.
- Télégramme 1 : 123 groupes, **615 lettres** ; télégramme 2 : 32 groupes, **160 lettres**. Transcriptions
  concordantes avec R. Bean (empreintes SHA-256 des lettres en capitales : `e266615d…a434c55` et `8fd5cfb8…e17a644`).
- Indice de coïncidence 0,0695 et 0,071, aucune structure de bigrammes : **transposition** d'un texte de type
  espagnol télégraphique.

## État de l'art (Bourdeau, septembre 2026)
Exclus, avec contrôles plantés : routes, barrière, décimation, colonnes simples (toutes largeurs, par un balayage des
écarts), double transposition inversée et mixte, **double transposition directe pour w2 ≤ 10 (toutes les clés) et
w1 ≤ 41**. Ouvert : double transposition directe avec **deux clés de 11 lettres ou plus** — la pratique allemande
(*Doppelwürfel*, deux phrases-clés de 15 à 25 lettres). Bourdeau a constaté, comme nous en D01 (dct_reloaded), que le
recuit sur K2 ne trouve pas la clé (paysage en « aiguille »).

## Ce que nous avons fait (4 octobre 2026)
Outil : `tools/bdt.c` (C, OpenMP), attaque conjointe des deux télégrammes (mêmes clés), contrôles plantés en espagnol
« télégraphique » (`tools/telegraphese.py`, `data/heldout/tg_es_58221.txt`). Résumé des cellules ci-dessous ; les
points saillants :
- **Correction de l'existant** : le balayage des écarts ne renseigne pas sur la double transposition directe (les
  contrôles de Bourdeau reposaient sur un clair répétitif) ; T1 y est parfaitement typique (B00).
- **Pourquoi le recuit échoue** au-delà de w2 ≈ 15 : avec K1 connue le paysage de K2 est lisse ; c'est le re-choix de
  K1 par l'IDP qui crée l'« aiguille » (mesuré, B00 §5). Même diagnostic sur le défi Schmeh 2007.
- **Deux conventions sont faciles même avec de longues clés** (inversée, colonnes-puis-lignes : voisins du clair à
  l'écart w1 quel que soit K1) et une troisième nettement plus facile (lignes-puis-colonnes) : B05.

## Données
`data/telegram1_615.txt`, `data/telegram2_160.txt` : transcriptions de D. Bourdeau (`ct1.txt`, `ct2.txt`), document
historique de 1937 ; recopiées avec mention de la source.

## Cellules
| Cellule | Question | Résultat |
|---|---|---|
| [B01 phrases Wikiquote es/de](experiments/B01_phrases_wikiquote/RESULTS.md) (pré-inscrit) | K2 est-elle le début d'une phrase espagnole ou allemande de Wikiquote ? | **non** : 5,4 M clés, IDP max 0,185 (seuil 0,28 ; contrôles 0,35–0,36) |
| [B00 vérifications](experiments/B00_constats/RESULTS.md) | colonne simple, transposition périodique, motifs T1/T2, paysage | colonne simple et périodique **exclues** (z max 2,2 / 2,3 contre 10,7 / 15,4) ; aucun motif ; balayage d'écarts non informatif |
| [B02 dictionnaire conjoint](experiments/B02_dictionnaire_conjoint/RESULTS.md) (pré-inscrit) | K2 ou clé unique = début de verset biblique (de/es) ou de phrase de 33 œuvres ? | **non** : 10,4 M clés, z max 6,1 (contrôles 21–25) ; + 730 clés thématiques, 64 k dates : rien |
| [B04 T2 seul](experiments/B04_T2_seul/RESULTS.md) | T2 chiffré avec ses propres clés courtes ? | **non** pour w2 ≤ 10 × w1 ≤ 16 (exhaustif) et clé unique w ≤ 12 |
| [B05 autres conventions](experiments/B05_autres_conventions/RESULTS.md) | inversée / mixtes avec longues clés | en cours |
| B03 recuit (pré-inscrit) | clé unique w = 11–30 ; deux clés w2 = 11–15 | en cours (GitHub Actions) |

