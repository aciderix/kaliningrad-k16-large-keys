# K16 — contrôles préliminaires, largeurs 10–14

Date : 2026-09-29.

## Préparation du flux réel

La transcription contient 984 lettres après translittération des caractères accentués
(`ê→e`, `ö→o`, `ü→u`). Le suffixe final `eimat` est exclu de la recherche, conformément
à la longueur de 979 lettres prévue dans le protocole. Les étiquettes de lignes et les
commentaires ne font pas partie du flux.

## Contrôle de puissance limité aux largeurs 10–14

Commande logique : `ctrl`, 10 essais, largeurs inconnues 10–14, `R2=3`, `I2=40000`,
`R1=5`, `I1=20000`, graine 31977. Modèle : quadrigrammes allemands fourni par le dépôt
`dagapeyeff`. Le contrôle est réussi si le solveur recolle au moins 90 % des 978
voisinages du clair.

| Essai | Largeurs plantées | Largeurs trouvées | Score | Contacts | Résultat |
|---:|:---:|:---:|---:|---:|:---:|
| 0 | 12,10 | 12,10 | −9,3639 | 978/978 | réussi |
| 1 | 12,14 | 12,14 | −14,0138 | 315/978 | échec |
| 2 | 13,10 | 13,10 | −9,2057 | 978/978 | réussi |
| 3 | 11,10 | 11,10 | −9,2812 | 978/978 | réussi |
| 4 | 11,13 | 11,13 | −9,0130 | 978/978 | réussi |
| 5 | 11,13 | 11,13 | −12,7349 | 555/978 | échec |
| 6 | 11,13 | 11,13 | −9,0691 | 978/978 | réussi |
| 7 | 12,14 | 12,14 | −11,2547 | 720/978 | échec |
| 8 | 13,11 | 13,11 | −9,2893 | 978/978 | réussi |
| 9 | 14,12 | 14,12 | −9,2619 | 978/978 | réussi |

**Résultat : 7/10**, sous le seuil de 8/10. Les essais 1, 5 et 7 avaient des
largeurs correctes mais n'ont pas retrouvé la seconde clé de permutation.

Ce lot ne couvre que les largeurs 10–14 et constitue un contrôle préliminaire, pas
le contrôle complet 10–20 prévu dans `PREREGISTRATION.md`. Il n'établit pas la
puissance du solveur, même dans la portée 10–14.

## Recherche exploratoire sur la bouteille

À la demande de l'utilisateur, le texte réel a néanmoins été testé malgré le résultat
de contrôle inférieur au seuil. Cette dérogation au protocole est explicite : les
résultats ci-dessous sont exploratoires et ne valident pas la famille cryptographique.

Le solveur a été compilé avec `-O3` et exécuté sur les largeurs 10–14 avec trois
graines indépendantes, `R2=12`, `I2=200000`, `R1=5`, `I1=20000`, `T2A=0.02`,
`T2B=0.001`.

| Graine | Score quadrigramme | Largeurs trouvées | Début du texte récupéré |
|---:|---:|:---:|:---|
| 20260929 | −12,1518 | 13,12 | `xftertalittdareterhausstdaimmuxmokpcpc` |
| 20260930 | −12,0278 | 13,11 | `xpmkpxmamtsoralitedecretistatdrauchuft` |
| 20261001 | −11,9771 | 13,12 | `fxtmpkumdariterstatexdalstmichatercoup` |

Les trois sorties sont illisibles et le meilleur score (−11,9771) reste sous le seuil
prévu de −10,5.

Deux flux nuls ont été exécutés avec le même réglage : −11,5668 et −12,0376. Le
premier dépasse le meilleur score réel; le second est légèrement inférieur. Le lot
prévu de 20 nuls n'a pas été terminé : après ces deux résultats, il ne pouvait pas
transformer les sorties réelles sous le seuil en solution, et ne servirait qu'à
affiner le classement statistique. Aucun p-value ni exclusion formelle n'est donc
rapporté.

**Conclusion exploratoire :** cette recherche n'a pas résolu le texte comme double
transposition allemande de largeurs 10–14. Elle ne permet pas d'exclure cette famille,
car le contrôle de puissance a donné 7/10 au lieu des 8/10 requis.

## Contrôles de largeurs inconnues 15–20 après correction du solveur

Le défaut d'enregistrement du meilleur candidat initial décrit dans
`AMENDMENT_2026-09-29.md` a été corrigé. Les réglages renforcés ont ensuite été
évalués sur six contrôles indépendants, avec une largeur inconnue tirée entre 15 et
20, `K16_SCREEN=3,60000,8`, `R2=12`, `I2=200000`, `R1=5`, `I1=20000`,
`T2A=0.02`, `T2B=0.001`.

| Graine | Largeurs plantées | Largeurs trouvées | Score | Contacts | Réussi (≥90 %) |
|---:|:---:|:---:|---:|---:|:---:|
| 61520 | 17,16 | 17,16 | −11,3422 | 746/978 | non |
| 61521 | 17,17 | 20,20 | −14,5021 | 6/978 | non |
| 61522 | 18,20 | 18,20 | −14,6271 | 57/978 | non |
| 61523 | 16,15 | 16,15 | −10,8546 | 795/978 | non |
| 61524 | 15,17 | 15,17 | −8,8937 | 978/978 | oui |
| 61525 | 17,15 | 17,15 | −13,9282 | 223/978 | non |

Résultat provisoire : **1/6**. Comme il reste quatre essais au plan initial,
même quatre succès supplémentaires n'atteindraient pas le seuil de 8/10. Le critère
de puissance échoue donc déjà mathématiquement; les contrôles restants et la recherche
sur la bouteille à largeurs 15–20 ne sont pas lancés. Ces données indiquent que le
criblage et le budget profond actuels ne récupèrent pas fiablement les clés de cette
plage. Elles ne disent rien, à elles seules, sur l'existence d'un clair sous-jacent.

## Optimisation OpenMP et vérification ciblée

Le solveur a été compilé avec `-O3 -march=native -flto -fopenmp`. Le criblage et les
recherches profondes répartissent les paires de largeurs entre les fils; les
redémarrages K1/K2 d'une paire connue sont aussi parallélisés. Le calcul garde les
mêmes nombres de redémarrages et d'itérations. Le score de chaîne évite un parcours
répété des ancêtres, et les températures sont précalculées pour conserver les mêmes
valeurs tout en évitant des appels répétés à `pow`.

Pendant la première version parallèle, le tableau temporaire IDP était encore partagé
entre les fils. Cette course a été corrigée en le rendant local à chaque fil. L'état
aléatoire a également été rendu indépendant et stable par tâche; les égalités sont
départagées par indice.

Deux contrôles renforcés déterministes à largeurs connues 17×16, même graine 77331,
ont ensuite produit le même résultat : **978/978 contacts**, score −9,3176, identique
au clair planté. Chaque exécution a demandé environ 4–6 minutes sur le téléphone.
Cela vérifie la récupération quand les largeurs sont connues, pas le criblage des 36
paires.

Un contrôle complet à largeurs inconnues 15–20 (graine 61520, `K16_SCREEN=3,60000,8`,
réglages profonds inchangés) a été interrompu après environ 18 minutes, avant que le
premier essai ne rende un résultat. Le téléphone ralentissait sous charge prolongée.
Il ne compte donc ni comme succès ni comme échec. Le taux 15–20 à largeurs inconnues
reste celui du lot sériel antérieur : **1/6**. L'optimisation n'a pas encore démontré
qu'elle rende ce protocole complet praticable en moins d'heures sur ce matériel.

## Contrôles 15–20 sur GitHub Actions

Run public : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36689646589>.
Dix contrôles indépendants ont tourné en parallèle sur des runners Ubuntu, avec quatre
fils chacun, le criblage `K16_SCREEN=3,60000,8` et les mêmes budgets profonds.
Chaque job a duré environ 17 à 24 minutes. Le solveur recompilé inclut les corrections
de course sur l'état IDP et sur les graines aléatoires.

| Graine | Largeurs plantées | Largeurs trouvées | Score | Contacts | Réussi (≥90 %) |
|---:|:---:|:---:|---:|---:|:---:|
| 61520 | 17,16 | 20,20 | −14,4730 | 10/978 | non |
| 61521 | 17,17 | 20,15 | −14,6492 | 2/978 | non |
| 61522 | 18,20 | 20,20 | −14,5555 | 2/978 | non |
| 61523 | 16,15 | 16,15 | −9,2250 | 978/978 | oui |
| 61524 | 15,17 | 15,17 | −10,4106 | 796/978 | non |
| 61525 | 17,15 | 18,20 | −14,3258 | 0/978 | non |
| 61526 | 18,17 | 20,20 | −14,5694 | 4/978 | non |
| 61527 | 20,15 | 20,15 | −10,6838 | 832/978 | non |
| 61528 | 15,16 | 15,16 | −9,0915 | 978/978 | oui |
| 61529 | 16,20 | 20,20 | −14,7447 | 4/978 | non |

Résultat : **2/10, soit 20 %**, sous le seuil de 8/10. Le job de recherche sur le
texte réel a donc été ignoré par la barrière de puissance. Cela laisse la plage
15–20 non testée sur le cryptogramme et ne permet aucune conclusion sur cette
hypothèse. Les journaux complets sont téléchargeables depuis le run ci-dessus.

## Recherche sans présélection, 10 contrôles

Run : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36696651221>.
Les largeurs 15–20 ont toutes été recherchées en profondeur (`R2=12`, `I2=200000`,
`R1=5`, `I1=20000`), sans le criblage top-8. Critère : au moins 90 % des 978
contacts. Les dix contrôles sont terminés; les journaux sont dans les artefacts du
run.

| Graine | Largeurs plantées | Largeurs trouvées | Score | Contacts | Réussi |
|---:|:---:|:---:|---:|---:|:---:|
| 62520 | 15,20 | 19,19 | −14,4980 | 3/978 | non |
| 62521 | 15,19 | 20,20 | −14,2590 | 6/978 | non |
| 62522 | 20,19 | 20,19 | −14,4793 | 8/978 | non |
| 62523 | 15,20 | 15,20 | −14,4087 | 214/978 | non |
| 62524 | 20,20 | 20,20 | −14,3107 | 156/978 | non |
| 62525 | 20,20 | 20,20 | −9,1228 | 978/978 | oui |
| 62526 | 19,17 | 19,17 | −10,5284 | 823/978 | non |
| 62527 | 17,15 | 17,15 | −9,1311 | 978/978 | oui |
| 62528 | 18,18 | 18,18 | −14,0400 | 193/978 | non |
| 62529 | 16,15 | 16,15 | −9,1302 | 978/978 | oui |

Résultat : **3/10**, soit 30 %. Le contrôle planté 19,17 retrouve exactement les
deux largeurs, mais sa permutation ne passe pas le seuil des contacts; dans d'autres
échecs la paire est incorrecte ou K2 ne donne pas le clair. Le seuil 10/10 n'est pas
atteint avec une recherche par contrôle.

## Répétitions indépendantes par contrôle : arrêt après diagnostic

Run : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36704467220>.
Dix nouveaux cryptogrammes de contrôle fixes, graines 63520–63529, reçoivent chacun
vingt recherches indépendantes avec des graines distinctes, sans changer le clair,
le modèle, le budget ou la plage des largeurs. Une exécution est retenue par contrôle
au score quadrigramme allemand maximal, puis évaluée selon le même seuil des contacts.
200 jobs ont été soumis à GitHub Actions, avec jusqu'à vingt runners Ubuntu distincts
actifs simultanément et quatre threads par job. La campagne a été arrêtée après
environ 3 h 30, une fois les journaux de 60 recherches récupérés; les jobs inachevés
ont été annulés pour réorienter le travail vers le défaut observé.

| Contrôle fixe | Clair planté | Recherches terminées | Succès individuels | Meilleur résultat (contacts) | Verdict du meilleur des 20 |
|---:|:---:|---:|---:|---:|:---:|
| 63520 | 16,16 | 20/20 | 15/20 | 978/978 | passe |
| 63521 | 16,20 | 20/20 | 0/20 | 334/978 | échoue |
| 63522 | 17,19 | 20/20 | 1/20 | 978/978 | passe |

À retenir : sur le cas 16×20, les largeurs trouvées par la meilleure recherche sont
exactes, mais la permutation de clé ne récupère que 334 contacts. Les répétitions ne
corrigent donc pas systématiquement l'échec de K2; augmenter le nombre de jobs n'est
pas la prochaine étape utile. Il faut diagnostiquer et améliorer la recherche K2 sur
des contrôles ciblés.

## Vérification directe du flux réel et correction du chargeur de fichier

Date : 2026-09-30. Une vérification directe a révélé un défaut dans la commande
`solve` : contrairement à ce qu'indiquait son usage, elle interprétait son troisième
argument comme le texte chiffré lui-même, et non comme un chemin de fichier. Un appel
avec `data/ciphertext_979.txt` n'analysait donc que les lettres du chemin. Le même
défaut touchait `null`. Les scores −9,93 du premier essai et les scores nuls associés,
produits pendant cette vérification, sont invalides et doivent être ignorés.

Le chargeur lit maintenant les lettres depuis le fichier; `solve` affiche la sortie
complète. Après recompilation, le fichier a été testé directement sur les 979 lettres
du flux :

| Recherche | Réglages | Score | Largeurs | Durée observée | Lecture du résultat |
|---|---|---:|:---:|---:|---|
| Recherche standard 10–14 | R2=3, I2=40000, R1=5, I1=20000 | −14,4665 | 14×11 | ~73 s | sortie illisible |
| K2 glouton + polissage, 10–14 | mêmes paramètres nominaux; mode expérimental | −14,4059 | 14×14 | ~7 s | sortie illisible |
| K2 glouton + polissage, 15–20 | R2=10, I2=40000, R1=5, I1=20000 | −14,2963 | 20×19 | ~38 s | sortie illisible |

Le meilleur clair connu produit un score autour de −9,3. Ces scores à −14,3 à
−14,5 ne ressemblent donc pas à un allemand récupéré. Le mode glouton est un outil
de tri rapide, pas une attaque validée : ses résultats 15–20 ne permettent pas
d'exclure formellement la double transposition. Aucune clé ni aucun texte clair n'a
été retrouvé. L'essai montre toutefois qu'on peut éliminer vite les candidats
manifestement mauvais avant d'envisager une recherche approfondie.

**Limite de validation :** le bug concerne les essais `solve` et `null` de cette
session; les commandes de contrôle ouvraient déjà leurs fichiers explicitement. Les
anciens résultats de contrôle et journaux GitHub ne sont pas modifiés par cette
correction.

## Recherche standard 15–20 découpée sur GitHub

Le 2026-09-30, le workflow a été remplacé par 36 jobs, un pour chaque paire de
largeurs 15–20, avec une recherche standard par paire (`R2=12`, `I2=200000`,
`R1=5`, `I1=20000`). Jusqu'à 20 runners tournent en même temps. Le chargeur corrigé
lit `ciphertext_979.txt` (979 lettres); chaque artefact contient le texte complet et
les clés. Les 36 jobs et le résumé se sont achevés en environ six minutes.

Run : <https://github.com/aciderix/kaliningrad-k16-large-keys/actions/runs/36733015575>.

| Rang | Largeurs | Score quadrigramme allemand |
|---:|:---:|---:|
| 1 | 19×20 | −14,2542 |
| 2 | 20×20 | −14,3784 |
| 3 | 18×18 | −14,3853 |
| 4 | 18×17 | −14,3868 |
| 5 | 20×17 | −14,4066 |

Le texte candidat du premier rang commence par
`lewzieisieheeuttelralfweifnrgdeanronrrevfcwnnszlswunlsnanebdeerwfemlirsrf`;
il n'est pas lisible comme allemand. Tous les 36 scores sont compris entre −14,2542
et −14,6676. Les contrôles où l'allemand a réellement été retrouvé donnent environ
−9,3; toutefois, les contrôles de puissance antérieurs n'atteignaient que 3/10. Le
solveur échoue donc souvent même sur un vrai clair allemand. Les scores faibles de
cette recherche signifient « aucun clair trouvé », mais ne distinguent pas sûrement
un faux texte d'un échec de l'algorithme.

Conclusion : la passe standard n'a pas résolu la bouteille et ne permet pas
d'exclure la double transposition allemande. Les artefacts GitHub conservent chaque
texte et chaque paire de clés pour vérification. Une preuve négative demanderait
d'abord une attaque qui passe correctement ses contrôles sur les largeurs 15–20.
