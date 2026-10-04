# B04 — Le second télégramme seul, avec ses propres clés courtes (4 octobre 2026)

**Hypothèse.** T2 (160 lettres, envoyé six heures après T1) n'utilise pas les clés de T1 mais des clés courtes à lui.
Personne ne l'avait testé : l'énumération exhaustive de Bourdeau porte sur T1.

**1. Deux clés, w2 = 2–10 (toutes les K2, 10! = 3,6 M pour w2 = 10) × w1 = 2–16.** `bdt exh` : IDP de T2 pour chaque
K2, les 10 meilleures K2 de chaque paire de largeurs passent à l'étape K1 (recuit aux quadrigrammes, 4 × 60 k).
- Contrôle planté (espagnol télégraphique, 160 lettres, K1 9 lettres, K2 8) : trouvé à (9, 8), clair lisible
  (« …en casa x detuvieron se dioses ocho dos dadores bienes umbral risa inextinguible… »), note **−9,74** ; toutes les
  fausses paires ≤ −12,4 (une fausse paire avait pourtant la plus haute IDP : l'étape K1 tranche).
- T2 réel : meilleur clair **−11,71** (« ciefengadabaeptal… »), au niveau du bruit. Journal : `logs/exh_w2_2-10_w1_2-16.out`.
- **Exclu** : T2 chiffré par double transposition directe avec w2 ≤ 10 et w1 ≤ 16 (pour w1 ≥ 12, l'IDP sur 160 lettres
  faiblit, z vrai 3,5–7 ; couverture partielle).

**2. Clé unique (K1 = K2), w = 5–25.** `bdt samescan` sur T2 seul, 32 recuits × 200 k par largeur.
- Contrôles plantés : w = 8, 10, 12 retrouvés (z = 10,9–12,2, note −9,97) ; **w = 14 manqué** (−12,8).
- T2 réel : z ≤ 5,8 et note ≤ −12,58 pour w ≤ 12 → **exclu pour w ≤ 12** ; au-delà, non concluant.
  Journal : `logs/samescan_T2_w5-25.out`.
