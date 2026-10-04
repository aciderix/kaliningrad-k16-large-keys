# K14 — RÉSULTATS (2026-09-29) : pas de double transposition « même clé » (Übchi) de 10 à 15 colonnes ; clés différentes longues **hors de portée**

Pré-inscription : `PREREGISTRATION.md` (commit e5df2d6) + amendement 1 (avant tout calcul sur la bouteille). Outils :
`tools/k14_double_idp.c` (diviser pour régner) ; `tools/k08_double_mi.c` (option même clé). Sorties : `logs/`.

## 1. Double transposition à deux clés différentes de 10 à 20 colonnes — **sans puissance**
Le score de juxtaposition des colonnes reconnaît la vraie seconde clé (−5,16 à −5,33 contre −5,5 à −5,8 pour la clé trouvée et
−5,8 à −6,1 au hasard), mais la recherche ne la retrouve qu'exceptionnellement (1 sur 4 à largeurs connues, même avec 80 000
itérations et température réglée ; aucune au-delà de 16 colonnes pour la seconde clé). Conformément à la règle, **non appliquée à la
bouteille** : cette famille n'est ni confirmée ni exclue.

## 2. « Même clé deux fois » (Übchi), 10-15 colonnes, largeur inconnue
Contrôles : quadrigrammes (lettres intactes) **9/10** ; MI (substitution admise) 6/10 ⇒ sans puissance, non interprété.
Bouteille (quadrigrammes) : meilleur −14,69 (w = 14) ; 20 nuls : −14,51 à −14,75 ; 13 nuls ≥ réel ⇒ p ≈ 0.67.
Un vrai texte remis en ordre score vers −9. Texte obtenu illisible.

## 3. Conclusion (RÉSULTAT)
- Double transposition à clé répétée (Übchi), 10-15 colonnes, lettres intactes : **exclue**.
- Double transposition à deux clés différentes ≥ 10 colonnes, et à clé répétée ≥ 16 colonnes : **hors de portée de nos outils**
  (sans puissance sur des messages plantés) — c'est désormais la frontière de ce qui peut être testé ici.
