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

## Ce que nous pouvons apporter
Notre étalonnage `dct_reloaded/experiments/D01` montre que l'**attaque par dictionnaire de phrases** (note IDP de la
seule K2) casse une double transposition 21×23 de 599 lettres quand la phrase-clé est dans la liste, là où le recuit
échoue. Ici les deux télégrammes ont probablement les mêmes clés : une K2 candidate doit relever l'IDP **des deux**.
Plan : modèle espagnol ; contrôles plantés (615 + 160 lettres, clés-phrases de 12–30 lettres) ; dictionnaires de
phrases espagnoles et allemandes (Wikiquote es/de, expressions courantes, devises).

## Données
`data/telegram1_615.txt`, `data/telegram2_160.txt` : transcriptions de D. Bourdeau (`ct1.txt`, `ct2.txt`), document
historique de 1937 ; recopiées avec mention de la source.

## Cellules
| Cellule | Question | Résultat |
|---|---|---|
| [B01 phrases Wikiquote es/de](experiments/B01_phrases_wikiquote/PREREGISTRATION.md) (pré-inscrit) | K2 est-elle le début d'une phrase espagnole ou allemande de Wikiquote ? | en attente de calcul |
