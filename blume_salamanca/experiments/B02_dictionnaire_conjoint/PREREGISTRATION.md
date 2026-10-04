# B02 — Phrases-clés allemandes et espagnoles, attaque conjointe des deux télégrammes (pré-inscription)

**Question.** K2 (et K1) sont-elles des débuts de versets bibliques (Luther 1545 modernisée, Elberfelder 1905,
Reina-Valera 1909 et 1865) ou des débuts de phrases et de vers de 33 œuvres allemandes et espagnoles du domaine
public (Faust, Werther, Buddenbrooks, Zarathoustra, Don Quichotte, La Regenta, Libro de Buen Amor…) ?

**Méthode.** `tools/bdt.c`, mode `dict` (bigrammes PMI espagnols tirés de `data/models/qg_es.bin`). Chaque clé
(11 à 30 lettres ; troncatures à chaque longueur et coupes aux mots, `tools/keys_texts.py`) est essayée :
1. comme K2, pour chaque w1 de 11 à 30 : IDP de T1, en score z contre 200 K2 aléatoires de même largeur ;
2. comme clé unique (K1 = K2, type ÜBCHI) : quadrigrammes des deux clairs complets, en score z contre 300 clés aléatoires.
Les touches au-dessus de z = 4,5 sont gardées ; pour les meilleures, z de l'IDP de T2 sous la même K2.

**Contrôles plantés (avant le calcul réel).** Espagnol télégraphique (`tools/telegraphese.py`, texte réservé
pg58221), 615 + 160 lettres, mêmes clés, clés-versets cachées parmi 20 000 clés bibliques :
- deux clés (K1 16 lettres, K2 11) : vraie K2 à z = 21,3, meilleure fausse 5,2 ;
- clé unique (11 lettres) : z = 25,1 (clé unique) et 23,8 (IDP).

**Décision (fixée avant le calcul).** Candidat si z(T1) ≥ 9 (l'un ou l'autre mode). Un candidat n'est retenu que si
l'étape K1 (recuit quadrigrammes) donne un clair espagnol lisible pour T1 **et** T2 sous les mêmes clés. Sinon :
« aucune clé de ces sources », sans autre conclusion sur le système.

**Calcul.** GitHub Actions (`.github/workflows/bdt-dict.yml`, 20 machines), environ 10,5 M de clés.
