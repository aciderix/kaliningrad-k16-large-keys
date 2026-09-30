# Avenant expérimental K16 — 2026-09-29

## Défaut trouvé et correction

La recherche K2 et la recherche K1 n'enregistraient pas leur permutation initiale
comme meilleure solution. Si aucune permutation voisine ne la dépassait, la sortie
pouvait rester non initialisée. Le solveur enregistre désormais aussi le meilleur
candidat initial de chaque étape. Aucun mouvement, score ni budget n'a été retiré.

Un mode de contrôle `ctrlpair` a été ajouté pour planter séparément les deux largeurs
et mesurer les cas ciblés sans criblage parasite.

## Contrôles ciblés prévus

Paires : 11×13 et 12×14. Pour chaque paire, comparer dix contrôles indépendants aux
réglages précédents (`R2=3`, `I2=40000`, `R1=5`, `I1=20000`) et dix contrôles avec
recherche K2 renforcée (`R2=12`, `I2=200000`, `R1=5`, `I1=20000`, `T2A=0.02`,
`T2B=0.001`). Succès : au moins 90 % des 978 voisinages récupérés.

Les largeurs 15–20 seront testées ensuite avec des contrôles à largeurs inconnues et
des permutations nulles, avant toute interprétation de la bouteille dans cette
portée. Les réglages seront consignés avant chaque lot; aucun réglage ne sera choisi
sur le score de la bouteille.

## Portée 15–20 : réglages gelés avant contrôle

- Contrôles : 10 textes allemands plantés; w1,w2 indépendants et uniformes dans
  15–20; largeur inconnue au solveur; les six premiers lots ont été lancés avec
  les graines 61520–61525 (la première valeur de graine avait été notée 51520
  dans la préinscription; l'écart est consigné et ne change pas le protocole).
- Criblage : `K16_SCREEN=3,60000,8` (36 paires classées, huit retenues).
- Recherche profonde : `R2=12`, `I2=200000`, `R1=5`, `I1=20000`,
  `T2A=0.02`, `T2B=0.001`.
- Critère : au moins 8/10 contrôles réussis avec 90 % des voisinages reconstruits.
- Si le seuil passe, bouteille puis 20 permutations nulles avec le même pipeline et
  les mêmes réglages. Si le seuil échoue, aucun résultat réel de cette portée ne sera
  interprété.

## Résultat et arrêt

Six essais terminés : 1/6 a reconstruit au moins 90 % des voisinages. Même si les
quatre essais restants réussissaient, le résultat final ne pourrait dépasser 5/10,
donc le seuil préétabli de 8/10 est hors d'atteinte. Le lot a été arrêté après six
essais; aucune recherche sur la bouteille à largeurs 15–20 n'est lancée, conformément
au critère d'arrêt ci-dessus. Les résultats sont consignés dans `RESULTS.md`.

## Optimisation du temps d'exécution

Le solveur a été modifié pour compiler avec OpenMP. Les paires de largeurs examinées
au criblage et à l'étape profonde sont indépendantes et distribuées entre les fils;
pour une paire fixée, les redémarrages K2 et K1 sont également distribués. Le calcul
garde le même nombre d'itérations et de redémarrages. Les tableaux temporaires du
score IDP et l'état aléatoire sont maintenant propres à chaque fil, avec graines
stables et départage déterministe des scores égaux.

Le score de chaîne IDP évite maintenant de reconstruire la liste des ancêtres pour
chaque voisin candidat : il compare directement la tête de chaîne, ce qui est
équivalent au test précédent. Les températures de recuit sont calculées une fois
par étape au lieu de recalculer `pow` pour chacun des redémarrages.

Compilation sur l'appareil : `gcc -std=c11 -O3 -march=native -flto -fopenmp -o
k16 tools/k16_double_ct2.c -lm`; exécution avec `OMP_NUM_THREADS=8`. Deux contrôles
à paire connue 17×16, mêmes paramètres renforcés et même graine, ont donné tous deux
978/978 contacts, score −9,3176 (score du clair −9,3176). Temps observé : environ
4–6 minutes par contrôle, variable avec la charge et la fréquence thermique.

Un contrôle 15–20 à largeurs inconnues avec le criblage complet a été lancé puis
interrompu après environ 18 minutes, avant la fin du premier essai, car le téléphone
ralentissait sous charge prolongée. Le gain exact face à une exécution sérielle n'a
pas été mesuré par un essai comparatif complet. Voir les résultats dans `RESULTS.md`.

Un contrôle complet de dix essais a ensuite été exécuté sur GitHub Actions, dix jobs
en parallèle et quatre fils par job. Résultat : **2/10** réussites selon le seuil des
90 % de contacts; la recherche sur le texte réel a été ignorée par le workflow. Voir
la table et le lien du run dans `RESULTS.md`.

## Nouvelle tentative visant 10/10

À la demande de l'utilisateur, le prochain lot vise 10/10. Le précédent échec montre
que les largeurs plantées étaient souvent éliminées par le criblage top-8. La
présélection est donc retirée : chacune des 36 paires (15–20 × 15–20) passe en
recherche approfondie. Les budgets par paire restent `R2=12`, `I2=200000`, `R1=5`,
`I1=20000`, `T2A=0.02`, `T2B=0.001`; les dix contrôles frais utilisent les graines
62520–62529. Critère de puissance courant : 10/10 avec au moins 90 % des contacts.
La recherche réelle est conditionnée à ce résultat. Dix jobs GitHub Actions sont
lancés en parallèle, quatre fils chacun; limite de temps configurée : six heures par
job. Réglages gelés avant le lancement du lot.

Run public : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36696651221>.
Le lot est terminé : **3/10** contrôles ont franchi le seuil. Le retrait du criblage
top-8 a amélioré le résultat de 2/10 à 3/10, mais les budgets de recherche profonde
ne suffisent toujours pas. Dans plusieurs contrôles en échec, la paire de largeurs
est trouvée mais la permutation K2 reste incorrecte.

## Campagne de répétitions visant 10/10

Une campagne distincte est lancée : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36704467220>.
Elle fixe dix nouveaux contrôles chiffrés (graines 63520–63529), puis lance vingt
recherches indépendantes par contrôle, soit 200 jobs. Chaque répétition conserve le
même cryptogramme et change seulement la graine de recherche; elle examine toutes les
36 paires 15–20 avec les budgets `R2=12`, `I2=200000`, `R1=5`, `I1=20000`. Pour chaque
contrôle, la solution retenue est celle ayant le meilleur score quadrigramme allemand
parmi les vingt recherches; le seuil de 90 % des contacts est évalué ensuite sur cette
solution. Jusqu'à vingt runners GitHub distincts exécutent quatre threads chacun.
Le gate demeure 10/10; aucune recherche sur la bouteille ne sera interprétée si le
gate échoue. Le mode `ctrlrep` a été compilé et vérifié avec un essai court avant la
campagne. La campagne a ensuite été annulée à la demande implicite de réorienter le
travail vers l'analyse, après récupération de 60 journaux sur 200. Les détails et le
tableau sont consignés dans `RESULTS.md`. Le contrôle planté 16×20 n'a passé le seuil
dans aucun de ses 20 essais, alors que la meilleure recherche retrouve les deux
largeurs exactes; la difficulté est la clé K2. Il n'est pas utile d'augmenter le
nombre de répétitions avant d'avoir amélioré cette étape.
