# K16 : contrôles des grandes clés

Ce dépôt dédié contient le solveur K16, le modèle allemand utilisé par le protocole,
le texte tenu à part pour les contrôles, et un workflow GitHub Actions manuel.

Le workflow manuel exécute une recherche standard par paire de largeurs (15–20), en
répartissant les 36 paires sur jusqu'à 20 runners. Chaque job examine le cryptogramme
réel et conserve le candidat, son score et ses clés en artefact. Cela évite les 200
recherches répétées du protocole de contrôle. La recherche reste exploratoire : les
contrôles précédents n'ont pas validé une récupération fiable pour toutes ces clés.

## Lancer les contrôles

Dans GitHub : **Actions → K16 parallel bottle scan → Run workflow**. Le résumé classe
les candidats par score quadrigramme allemand. Les artefacts contiennent le texte
complet et les deux permutations pour chaque paire.

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

## Recherche exploratoire sur un fichier

Les commandes `solve` et `null` prennent le chemin du fichier chiffré en troisième
argument. `solve` affiche tout le texte candidat. Vérifier la longueur du flux
(979 lettres pour cette expérience) avant d'interpréter un score. Le mode local
`K16_IDP_GREEDY=1 K16_K2_POLISH=1` est expérimental et ne remplace pas les contrôles
de puissance.
