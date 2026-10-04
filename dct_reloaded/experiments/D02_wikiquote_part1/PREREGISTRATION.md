# D02 — Partie 1 : K2 tirée d'une phrase de Wikiquote — pré-inscription (2026-10-04, avant le calcul sur la partie 1)

## Hypothèse
La clé K2 de *DCT Reloaded 1* (613 lettres, clés de 20–27 lettres, longueurs premières entre elles, « dérivées de
phrases anglaises ») est le début d'une phrase citée dans Wikiquote anglais : soit une suite de mots entiers depuis le
début de la phrase (base « prefix »), soit les 20 à 27 premières lettres de la phrase coupées n'importe où (base
« trunc »). Wikiquote n'est pas dans la base de G. Lasry (Wikipédia + Gutenberg, 2018).

## Données
Dump `enwikiquote-latest-pages-articles.xml.bz2` (219 Mo, téléchargé le 2026-10-04) → 148 982 pages, 7,52 millions
de phrases et fragments (`tools/wikiquote_extract.py`) → 8 481 956 clés « prefix » et 37 255 756 clés « trunc »
distinctes (`tools/wikiquote_keys.py`).

## Méthode
`dctsolve stream` : pour chaque clé de longueur w2 ∈ [20,27], K2 = rang alphabétique (ex aequo de gauche à droite,
convention validée en D01), IDP pour chaque w1 ∈ [20,27] premier avec w2 et différent ; note PMI (`DCT_PMI=1`).

## Contrôles (faits avant ce calcul, `logs/controles.out`)
5 chiffrés plantés (Frankenstein, 613 lettres, K1 et K2 tirées de la base « prefix », longueurs premières entre
elles), vraie K2 glissée parmi 200 000 leurres : **5/5 en tête**, IDP vraie 0,40–0,45 ; meilleur leurre ≤ 0,25.

## Critère (fixé maintenant)
- **Candidat** : IDP ≥ 0,30.
- **Déchiffrement** : pour un candidat, recherche de K1 par recuit (`withk2`, 8 × 50 000) donnant une note de
  quadrigrammes ≥ −10,5 **et** un texte anglais lisible. Les 34 premières lettres sont alors la solution demandée.
- Sinon : K2 n'est le début d'aucune phrase de Wikiquote (au sens des deux bases), avec une puissance de 5/5.

## Avenant (2026-10-04, avant tout résultat de ces bases)
Base supplémentaire « windows » : toute suite de mots entiers de 20 à 27 lettres, n'importe où dans la phrase.
Les bases « trunc » et « windows » sont calculées sur GitHub Actions (workflow `phrase-scan`, 20 machines, clés
générées par `common/phrasekeys.py`, réparties sans doublon par crc32 mod 20). Même note, mêmes largeurs, même
critère (IDP ≥ 0,30 puis K1 lisible).
