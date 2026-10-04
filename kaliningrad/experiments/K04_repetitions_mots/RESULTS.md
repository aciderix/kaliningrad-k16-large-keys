# K04 — RÉSULTATS (2026-09-29) : **les mots du chiffré ne sont pas les mots du clair** ; les espaces ont été posés après coup

Pré-inscription : `PREREGISTRATION.md` (commit 748171a). Outil : `tools/k04_repetitions.py` ; sortie : `logs/k04.out`.

## 1. Résultats
Chiffré (v1) : 194 mots, **D = 182** multiensembles de lettres distincts (seuls « i » ×7, « lel », « ê », « ue » et la paire
rande/eradn se répètent).

| Langue | fenêtres de 194 mots | D moyen | D max | fenêtres ≥ 182 |
|---|---|---|---|---|
| allemand | 3 393 | 130,4 | 157 | 0 |
| néerlandais | 3 769 | 129,0 | 155 | 0 |
| suédois / danois | 678 / 480 | 129,0 / 124,3 | 150 / 149 | 0 / 0 |
| français / italien / espagnol | 5 763 / 5 204 / 7 110 | 126,9 / 136,0 / 118,5 | 152 / 155 / 143 | 0 |
| espéranto | 4 916 | 121,1 | 154 | 0 |
| **russe** (Gutenberg 37196, 30774) | 96 | 151,5 | 171 | 0 |
| **polonais** / **tchèque** | 1 035 / 274 | 155,0 / 135,7 | 172 / 160 | 0 / 0 |
| finnois / hongrois (agglutinantes) | 382 / 201 | 156,1 / 151,1 | 175 / 172 | 0 / 0 |
| latin | 1 157 | 166,7 | 187 | 23 (toutes dans l'**Énéide**, vers épiques) |

Contrôle positif : allemand transposé (grille 13×13 à clé) puis recoupé en faux mots avec les longueurs de mots du chiffré :
D = 185 à 191 (moyenne 188,3) : **même ordre que le chiffré**.

## 2. Conclusion (RÉSULTAT)
- La famille « **mots du clair conservés** » (substitution fixe lettre à lettre, avec ou sans brouillage des lettres dans chaque
  mot) est **rejetée** pour les 13 langues en prose testées, y compris les plus flexionnelles (russe, polonais, finnois, hongrois).
  Seule la poésie épique latine atteint ce niveau, et le latin est par ailleurs exclu par son profil de fréquences sous toute
  substitution (K02 § 4 : p ≤ 0,003).
- Avec K02 : ni contacts entre lettres, ni mots répétés ⇒ **les espaces ne viennent pas du clair**. Ils ont été posés sur une
  suite de lettres déjà mélangée, mais pas au hasard (K02-T6) : un « i » isolé devient un mot, les grappes imprononçables de
  consonnes deviennent des abréviations (27 lettres d'abréviation, aucune voyelle), les mots finissent volontiers par n ou t.
  C'est le comportement de quelqu'un qui **habille** une suite de lettres pour qu'elle ressemble à une langue.
- Hypothèse A (texte transposé sur de grands blocs, espaces cosmétiques) **renforcée** ; B (pseudo-texte) reste possible.
