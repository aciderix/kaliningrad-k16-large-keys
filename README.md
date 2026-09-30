# K16: contrôles et recherche des grandes clés

Ce dépôt dédié contient le solveur K16, le modèle allemand utilisé par le protocole,
le texte tenu à part pour les contrôles, et un workflow GitHub Actions manuel.

Le workflow démarre dix contrôles indépendants sur des runners Ubuntu. Chaque runner
utilise ses quatre cœurs pour rechercher en profondeur les 36 paires de largeurs
15–20, sans présélection. Les dix journaux sont conservés en artefacts. La recherche
sur la bouteille ne part que si les dix contrôles satisfont le seuil de 90 % des
contacts.

## Lancer les contrôles

Dans GitHub : **Actions → K16 large-key controls → Run workflow**. Le workflow se
termine avec un résumé du nombre de contrôles récupérés. L'objectif courant est 10/10.
Les artefacts contiennent
les largeurs plantées et trouvées, les scores et les nombres de contacts.

## Données

- `data/transcription_v1.txt` : transcription de la bouteille.
- `data/models/qg_de.bin` : modèle quadrigramme allemand, 456 976 flottants float32.
- `data/heldout/de.txt` : texte indépendant du modèle, utilisé uniquement comme clair
  planté pour mesurer la puissance.
- `tools/prepare_cipher.py` produit les 979 lettres du flux de recherche en retirant
  le suffixe `eimat` conformément au protocole K16.

Les dix contrôles utilisent le même modèle, les mêmes budgets et le même criblage que
le protocole de recherche. Le workflow ne reçoit ni jeton ni secret GitHub.
