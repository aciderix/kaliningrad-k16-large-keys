# K16 : contrôles des grandes clés

Ce dépôt dédié contient le solveur K16, le modèle allemand utilisé par le protocole,
le texte tenu à part pour les contrôles, et un workflow GitHub Actions manuel.

Le workflow démarre 200 jobs sur des runners Ubuntu : dix contrôles chiffrés fixes,
avec vingt recherches indépendantes par contrôle. Chaque job utilise quatre threads
pour parcourir en profondeur les 36 paires de largeurs 15–20, sans présélection.
Pour chaque contrôle, le résultat retenu est celui dont le score allemand est le plus
élevé parmi les vingt graines de recherche; le seuil de contacts est ensuite mesuré
sur ce résultat. Les journaux sont conservés en artefacts. La recherche sur la
bouteille ne part que si les dix contrôles atteignent le seuil de 90 %.

## Lancer les contrôles

Dans GitHub : **Actions → K16 large-key controls → Run workflow**. Le résumé indique
les résultats retenus pour les dix contrôles. L'objectif courant est 10/10. Les
artefacts contiennent les largeurs plantées et trouvées, les scores et les contacts.

## Données

- `data/transcription_v1.txt` : transcription de la bouteille.
- `data/models/qg_de.bin` : modèle quadrigramme allemand, 456 976 flottants float32.
- `data/heldout/de.txt` : texte indépendant du modèle, utilisé uniquement comme clair
  planté pour mesurer la puissance.
- `tools/prepare_cipher.py` produit les 979 lettres du flux de recherche en retirant
  le suffixe `eimat` conformément au protocole K16.

Les contrôles utilisent le même modèle, les mêmes budgets et la recherche exhaustive
des largeurs que le protocole de recherche. Le workflow ne reçoit ni jeton ni secret
GitHub.
