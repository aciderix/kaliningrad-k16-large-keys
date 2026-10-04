# B05 — Les autres conventions de double transposition, avec de longues clés (4 octobre 2026)

F_K = colonne directe (écrire en lignes, lire les colonnes dans l'ordre de K) ; G_K = F_K⁻¹ (écrire en colonnes dans
l'ordre de K, lire en lignes). Quatre conventions : directe F_K2∘F_K1 (le *Doppelwürfel* classique), inversée
G_K2∘G_K1, mixte colonnes-puis-lignes F_K2∘G_K1, mixte lignes-puis-colonnes G_K2∘F_K1.

**Ce que l'existant couvrait.** Bourdeau : inversée exclue pour w1 × w2 < ≈ 560 (balayage des écarts : les voisins
tombent à l'écart w1·w2) ; les deux mixtes exclues pour w2 ≤ 10 (énumération). Au-delà : ouvert.

**Observation.** Deux de ces conventions ne sont pas des « aiguilles » :
- inversée : J = F_K2(C) = G_K1(P) ; colonnes-puis-lignes : J = F_K2⁻¹(C) = G_K1(P). Dans les deux cas, les voisins
  du clair sont à l'écart **w1** dans J **quelle que soit K1** : la note de K2 (bigrammes PMI à l'écart w1, T1 + T2)
  ne demande pas de deviner K1, et elle est lisse (comme une colonne simple) ;
- lignes-puis-colonnes : I = F_K2(C) = F_K1(P) ; défaire K2 ne fait que réordonner des colonnes **fixes** de C, si
  bien qu'une K2 partiellement juste laisse des colonnes de K1 entières intactes : l'IDP y est bien plus lisse qu'en
  convention directe.

## Inversée (`bdt lagscan2 … 0`)
Contrôle planté (espagnol télégraphique, 615 + 160 lettres, mêmes clés, K1 22 lettres, K2 26) : 4 recuits × 100 k →
bonne paire à **z = 17,8**, clair lisible (« funestos cuatro dos designios desposa no tardaron dioses revelar… ») ;
fausses paires z = 8–9,3.

BLUME, w1 et w2 = 11–40 (900 paires, 8 recuits × 100 k) : voir `logs/rev_w11-40.out` et le bilan ci-dessous.

## Lignes-puis-colonnes (`BDT_RC=1 bdt scan`)
Contrôle 18 × 19 : 4 recuits × 200 k → **trouvé** (z = 18,4 ; T1 et T2 lisibles), alors qu'en convention directe le
recuit échoue dès 16 × 17. Contrôle 23 × 24 : 4 recuits insuffisants (z = 11,8, partiel).

## Colonnes-puis-lignes
Note tolérante aux bornes (`lagscan2 … 2`, puis finition exacte) : contrôle 22 × 26 → z = 13,4, clair partiellement
lisible seulement. Cause structurelle : si pgcd(w1, w2) = g > 1, les liens c → c + w1 (mod w2) forment g cycles de
colonnes indépendants, dont la position relative n'est pas fixée par l'écart w1 ; il faut énumérer les rotations
relatives à l'étape K1. Non lancé sur BLUME (convention la moins probable).
