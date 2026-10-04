# K01 — RÉSULTATS (2026-09-28) : les trois hypothèses structurelles publiées sont **rejetées** ; contrôles réussis

Pré-inscription : `PREREGISTRATION.md` (commit e2e7f8f) + amendement 1 (commit aef807d, avant tout calcul sur le texte réel).
Outil : `tools/k01_structure.py` ; sorties : `logs/controles.out`, `logs/reel_v1.out`, `logs/reel_v0.out`.
Données : `data/transcription_v1.txt` (variante A : 26 lettres, apostrophes et soulignements ignorés).

## 1. Contrôles synthétiques (texte allemand réservé, blocs de 166/169/162/169/169/144 lettres)
| Contrôle | T1 χ² (p_bas) | T2 profils triés (p_bas) | T3 isomorphes (p_haut) | Attendu |
|---|---|---|---|---|
| (a) même bloc transposé 6 fois | 4,2 (**0,0001**) | 0,710 (**0,0001**) | 0,98 | T1, T2 petits ✓ |
| (b) même bloc, 6 substitutions | 952 (1,0) | 0,710 (**0,0001**) | **0,0033** | T2 petit, T3 grand ✓ |
| (c) 6 blocs différents, même substitution | 111 (0,56) | 2,720 (0,66) | 0,98 | hasard ✓ |

| Contrôle T4 (anagrammes, mots ≥ 4 lettres) | fraction allemande | null | p |
|---|---|---|---|
| (d) mots du lexique, anagrammés | 1,000 | 0,169 | 0,005 |
| (d′) mots d'un vrai texte allemand (Gutenberg 6343), anagrammés — ajouté avant le texte réel, plus exigeant | **0,888** | 0,122 | 0,005 (allemand ≫ nl 0,342, en 0,257…) |
| (e) mots allemands sous substitution | 0,017 | 0,020 | 0,69 (hasard ✓) |

⇒ Les quatre tests ont la puissance voulue (p minimaux atteignables : 1/10 001 ; T3 1/301 ; T4 1/201).

## 2. Texte réel
| Données | T1 χ² (p_bas) | T2 (p_bas) | T3 (p_haut) |
|---|---|---|---|
| v1, S1-S6 | 94,6 (0,23) | 2,729 (0,62) | 0,46 |
| v1, S1-S5 (sans la page 2 pâle) | 75,5 (0,25) | 1,838 (0,72) | 0,34 |
| v0, S1-S6 (sensibilité) | 108,8 (0,48) | 2,836 (0,72) | 0,55 |

T4 (v1, 137 mots ≥ 4 lettres) : allemand **0,197** (null 0,163, p = 0,16) ; nl 0,175 (0,33) ; en 0,146 (0,74) ; sv 0,153 (0,20) ;
da 0,146 (0,14) ; cs 0,131 (0,52) ; pl 0,117 (0,19) ; fr 0,153 (0,61) ; it 0,146 (0,20). v0 : même conclusion.

## 3. Conclusions (RÉSULTAT)
1. **« Le même passage chiffré 7 fois par transposition »** (hypothèse de T. Ernst, Cipherbrain 2017) : **rejeté**. Les sections
   ont des comptes de lettres aussi différents que des morceaux quelconques d'un même texte (χ² = 94,6 contre 4,2 pour le contrôle).
2. **« Le même passage sous une substitution différente par section »** : **rejeté** (ni profils triés semblables, ni isomorphes).
3. **« Des mots allemands dont les lettres sont mélangées »** (idée récurrente, Cipherbrain 2016 et commentaires russes 2015) :
   **rejeté** : 20 % des mots sont des anagrammes de mots allemands, ce qu'on obtient avec des mots aléatoires (16 %), alors qu'un vrai
   texte allemand anagrammé en donne 89 %. Aucune autre langue testée ne ressort non plus.
4. Le texte se comporte comme le contrôle (c) : **un seul texte continu, découpé en sections, avec une seule règle de
   lettres** (ou pas de chiffre au niveau des lettres). Portée : T4 ne dit rien si les espaces sont factices (transposition sur le
   bloc entier puis espaces arbitraires) ; ce cas n'est pas couvert par K01.
   **Précision apportée par K02** : l'homogénéité des sections n'implique pas une substitution lettre à lettre ; K02 montre que les
   lettres voisines ne sont pas liées, ce qui exclut une langue lue dans l'ordre (même substituée) : un texte **transposé** sur de
   grands blocs, ou un pseudo-texte, se comporte lui aussi comme le contrôle (c).

## 4. Observations (non testées ici, pour la suite)
- **IC** : en 26 lettres (variante A), IC = **0,083** ; avec lettre + apostrophe comme symbole distinct (35 symboles), 0,063. Le
  0,054 cité sur Cipherbrain (« compatible avec le russe ») portait sur ≈ 50 signes ; le comparer à l'IC du russe en 33 lettres
  cyrilliques (≈ 0,053) ne tient pas. 0,083 est dans la queue haute des textes allemands de 984 lettres (0,5 % à 7 % des blocs
  selon le corpus l'atteignent).
- **Fréquences** : e 17,2 % (allemand ≈ 17 %), mais n 13,9 % (≈ 10 %), f 4,7 % (≈ 1,7 %), a 4,1 % (≈ 6,5 %), o ≈ 1 % (≈ 2,5 %) :
  pas de l'allemand transposé tel quel. L'apostrophe suit surtout n (41/137), t (28/49), r, d : consonnes, jamais de voyelle.
- **Tailles des sections** : 169 = 13², 144 = 12² ; 166 et 162 en sont proches (lettres manquées à la copie, ou blocs incomplets).
  HYPOTHÈSE : transposition par grille carrée bloc par bloc (Schmeh évoquait déjà « block-wise transposition » ; la coïncidence avec
  des carrés n'a pas été trouvée dans les sources lues). Test naturel (à pré-inscrire, K02) : un excès de bigrammes « plausibles »
  à distance 13 (12 pour S6) dans chaque section.
