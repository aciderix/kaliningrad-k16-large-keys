# B02 — Résultats : phrases-clés bibliques et littéraires allemandes et espagnoles

**Calcul.** GitHub Actions, run 37190483289 (20 machines, ≈ 10 min de balayage chacune), 4 octobre 2026.
Sources : Luther (révision Bolsinger, 1545 modernisée), Elberfelder 1905, Reina-Valera 1909 et 1865
(scrollmapper/bible_databases) ; 33 livres Gutenberg allemands et espagnols (Faust I, Werther, Buddenbrooks,
Zarathoustra, Effi Briest, Der Zauberberg, Die Traumdeutung, Kritik der reinen Vernunft, Don Quijote, La Regenta,
Libro de Buen Amor, Niebla, El sombrero de tres picos…). Clés : débuts de verset, de ligne et de phrase, tronqués à
11–30 lettres et coupés aux mots (`tools/keys_texts.py`).

**Volume.** 10,39 M de clés ; 218 M d'essais (chaque clé comme K2 pour w1 = 11–30, et comme clé unique).

**Résultat.** Histogramme des z au-dessus de 4,5 : [4,5) : 2 043 ; [5,6) : 304 ; [6,7) : 2 ; rien au-delà.
Meilleur : z = 6,09 (« dijoleasuvezelhombreque », w1 = 12, w2 = 23, z(T2) = 0,1), au niveau attendu du maximum de
218 M essais gaussiens. Les contrôles plantés donnaient z = 21,3 (deux clés) et 25,1 (clé unique).

**Conclusion (seuil pré-inscrit z ≥ 9).** Aucune clé de ces sources n'est K2 (pour w1 = 11–30), ni la clé unique.
Rien n'est dit des autres sources de phrases.

**Compléments locaux (même mode `dict`).** 730 clés thématiques (`data/keys_thematiques.txt`) : aucun z > 4,5 ;
64 053 dates en toutes lettres (1936–1937, de/es/fr/en) : z max 5,4.

**Variante « ex aequo de droite à gauche » (`BDT_TIES=1`), locale.** 730 clés thématiques : aucun z > 4,5 ;
64 053 dates : z max 5,0. (Bibles, œuvres, Wikiquote et Gutenberg complet dans les deux numérotations : B07, GPU, rien.)
