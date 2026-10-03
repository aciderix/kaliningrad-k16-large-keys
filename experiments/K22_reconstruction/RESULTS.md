# K22 — Peut-on reconstituer le texte sans source ni original ? (2026-10-03)

Statut : exploration calibrée sur contrôles. Outils : `tools/k22/` ; sorties : `logs/`.
Contexte : l'auteur, les feuilles originales et un texte source étant hors d'atteinte, il restait deux voies :
deviner des mots (voie 4) ou reconstruire le texte avec un modèle de la langue plus fort que les fréquences de lettres
(voie 5).

## 1. Décodeur mot à mot sous contrainte de déplacement (`wdecode.py`, `ctrl22.py`)

Le clair est construit comme une suite de **vrais mots** (dictionnaire de 170 000 formes, modèle de paires de mots
appris sur 20,6 millions de mots de 420 livres allemands, Kafka exclu) ; chaque lettre doit être prise dans le flux à
moins de D positions, chaque position une seule fois (l'occurrence libre la plus à gauche ne fait perdre aucune
solution) ; recherche en faisceau (100 hypothèses). Contrôle : 200 lettres de Kafka (*Die Verwandlung*), lettres
déplacées au hasard d'au plus s positions.

| s | lettres à la bonne place | lecture | score du modèle : décodé / vrai texte |
|---:|---:|---|---:|
| 2 | 0,51 | « bloss mit und ja … **unnotige sorgen und versaumen** … **ihre geschaftlichen pflichten einer eigentlich** … **ich spreche** … **ihrer eltern und ihres chefs und bitte** » : récupération partielle | −249 / −261 |
| 4 | 0,14 | « **bloss mit** den juni nach einem alten herrn … **pflichten** … **ich spreche** … » : quelques mots | −231 / −261 |
| 10 | 0,10 | « mann nicht bloss den juwelieren meist nach einer strengen hausordnung … » : **allemand fluide mais faux** | −188 / −261 |

Dès s ≈ 4, le modèle trouve un texte qu'il juge **meilleur** que le vrai : ce n'est pas un défaut de recherche, mais
l'existence de nombreuses autres phrases compatibles. La bouteille, elle, n'a aucune paire de lettres voisines
conservée (K02) et une échelle estimée de 25 à 100 positions (K21) : très loin du domaine où la méthode fonctionne.

## 2. Mots devinés (`cribcheck.py`)

Proportion des positions de la bouteille où toutes les lettres d'un mot se trouvent dans une fenêtre compatible avec
un déplacement d'environ 50, comparée à 20 mélanges : Heimat 0,61 / 0,57 ; Schule 0,53 / 0,48 ; Mutter 0,55 / 0,53 ;
Freund 0,87 / 0,82 ; Deutschland 0,45 / 0,39 ; Krieg 0,21 / 0,17 ; Pillau 0,06 / 0,07 ; Moskau 0,16 / 0,13.
**Aucun mot ne se distingue du hasard** : à cette échelle, un mot deviné n'apporte pas d'information. Seule contrainte
dure : le clair ne contient ni j, ni q, ni x, ni y (« Baltijsk », « Sowjetunion » sont impossibles tels quels) ; et il
contient au plus 2 p, 3 v, 6 b, 7 k et 9 z.

## 3. Pourquoi : l'information sur l'ordre a disparu (`unicity.py`)

Un brassage local ne laisse, sur l'ordre, que la **composition** de chaque portion du texte. Information portée par
la composition de tranches de n lettres d'allemand (formule multinomiale, 3 000 tranches) :

| n | 3 | 5 | 10 | 25 | 50 | 100 | 170 |
|---|---:|---:|---:|---:|---:|---:|---:|
| bits par lettre | 3,3 | 2,8 | 2,2 | 1,4 | **0,9** | 0,6 | 0,4 |

Pour désigner un seul texte, cette information doit dépasser l'incertitude d'un texte allemand cohérent, **environ
1 à 1,3 bit par lettre** pour les meilleurs modèles de langue (ordre de grandeur des estimations de type Shannon).
- tranches de quelques lettres : 2 à 3 bits par lettre, le texte est déterminé (le contrôle s = 2 le retrouve) ;
- tranches de 50 lettres : 0,9 bit par lettre **dans le cas le plus favorable** (découpe connue, aucun nul, aucune
  erreur de lecture). Il manque au moins 0,1 à 0,4 bit par lettre, soit, sur 979 lettres, de l'ordre de 2¹⁰⁰ à 2⁴⁰⁰
  textes allemands cohérents tous compatibles avec la bouteille ; avec une découpe inconnue, des nuls et quelques
  erreurs, bien davantage.

## 4. Conclusion

Sans information extérieure (auteur, original, texte source), **le message ne peut pas être reconstitué, quelle que
soit la méthode** — statistique, mot à mot ou fondée sur le sens : à l'échelle de brassage mesurée, la bouteille
contient moins d'information sur l'ordre des lettres qu'il n'en faut pour distinguer le vrai texte de très nombreux
autres textes allemands cohérents. Une proposition de solution resterait **vérifiable** (mêmes lettres, déplacements
limités), mais aucune ne pourrait être prouvée unique. Seule exception : si l'échelle réelle était au bas de
l'intervalle estimé (≈ 25 lettres) et le texte sans nuls, l'information serait à la limite — ce que les contrôles du
§ 1 ne permettent pas d'exploiter avec les modèles disponibles ici.

## 5. Propositions « crédibles » pour la bouteille (`bottle22.py`, `shuf22.py`, `logs/bottle_decodes.out`)

Le décodeur appliqué au bloc 1 (166 lettres, nuls f/w/n autorisés) produit des phrases allemandes :
D = 25 : « die öffentliche Darstellung der Verhältnisse kennenlernte … Freundschaft … Landwirtschaft … » ;
D = 50 : « der niederländischen Residentschaft auf der deutschen Völkerschaften welche alle Errungenschaften unserer
Freundschaft mit fortlaufenden Nummern … ». Les **mêmes lettres mélangées au hasard** donnent des phrases du même
niveau : « den Traumgedanken enthalten Scheidewände … fest verschlossenen Fensterläden im nordwestlichen Deutschland und
fünfhundert Dollar … », « der demokratischen mitteldeutschen Handelsverein … am Fenster öffnen Fenster … ». Ces
propositions changent avec D, n'ont aucune cohérence d'ensemble et ne se distinguent pas de celles obtenues sur du
hasard : ce sont des textes **compatibles**, pas des déchiffrements.

## 6. Note sur l'échelle (20 ou 50 ?)

K19 avait estimé « une vingtaine de lettres » en comparant la bouteille à **un seul tirage** par contrôle. K21 a
repris l'estimation avec 3 000 simulations par modèle : médiane ≈ 55, intervalle à 90 % ≈ 25–100 (le repérage de mots
de K20 pointait aussi vers 40–80). C'est cette dernière valeur qui est retenue ; même à 20–25 lettres, la composition
locale ne porterait que ≈ 1,4–1,6 bit par lettre, à la limite de ce qu'il faut, et le décodeur échoue déjà à 10 (§ 1).
